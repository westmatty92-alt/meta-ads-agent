# Supabase Common Fixes & Gotchas
# Reference this whenever Supabase saves or loads are not working
# Last updated: June 2026

---

## 🔴 CRITICAL: Two Things Required for Every Upsert to Work

Every Supabase table that uses upsert MUST have BOTH of these or saves will silently fail:

### 1. UNIQUE constraint on the conflict column
Without this, upsert with onConflict fails with error code 42P10.

```sql
ALTER TABLE your_table ADD CONSTRAINT your_table_column_unique UNIQUE (column_name);
```

### 2. RLS policy WITH CHECK clause
Without WITH CHECK, inserts are blocked silently. No error shown to user — data just never saves.

WRONG (blocks inserts):
```sql
CREATE POLICY "name" ON table FOR ALL USING (auth.uid() = user_id);
```

CORRECT (allows inserts):
```sql
CREATE POLICY "name" ON table FOR ALL 
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

---

## 🐛 DEBUGGING CHECKLIST — When Data Is Not Saving

Run through this in order before touching any code:

### Step 1 — Check if data is reaching Supabase
In browser console:
```javascript
sb.from('your_table').upsert({
  your_column: 'test',
  user_id: currentUser.id
}, { onConflict: 'your_column' }).then(r => console.log('result:', r.data, 'error:', r.error))
```

### Step 2 — Check the error code
| Error code | Meaning | Fix |
|-----------|---------|-----|
| 42P10 | No unique constraint on conflict column | Add UNIQUE constraint |
| 42501 | RLS permission denied | Fix RLS policy WITH CHECK |
| PGRST116 | 0 rows returned on load | Data never saved, or wrong query |
| 23505 | Duplicate key violation | Row already exists, check onConflict |
| null error, null data | Save succeeded but no .select() chained | Add .select() or check table directly |

### Step 3 — Verify data in Supabase directly
```sql
SELECT * FROM your_table WHERE user_id = 'your-user-id';
```
If row exists — save worked, load is broken.
If no row — save is broken.

### Step 4 — Check RLS policies
```sql
SELECT policyname, cmd, qual, with_check 
FROM pg_policies 
WHERE tablename = 'your_table';
```
If with_check is null — fix the policy.

### Step 5 — Check unique constraints
```sql
SELECT constraint_name, column_name 
FROM information_schema.key_column_usage 
WHERE table_name = 'your_table';
```
If no unique constraint on your conflict column — add one.

---

## 📋 TEMPLATE: Complete Table Setup (Copy This Every Time)

```sql
-- 1. Create table
CREATE TABLE IF NOT EXISTS your_table (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  business_id uuid REFERENCES businesses(id) ON DELETE CASCADE,
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  -- your columns here
  updated_at timestamptz DEFAULT now()
);

-- 2. Add unique constraint for upsert
ALTER TABLE your_table ADD CONSTRAINT your_table_business_id_unique UNIQUE (business_id);

-- 3. Enable RLS
ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;

-- 4. Create policy WITH CHECK (critical)
CREATE POLICY "users_own_your_table" ON your_table
FOR ALL
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

---

## 📋 TEMPLATE: Fix Existing Table That Is Not Saving

Run this for any table that is failing to save:

```sql
-- Fix 1: Add unique constraint if missing
ALTER TABLE your_table ADD CONSTRAINT your_table_column_unique UNIQUE (conflict_column);

-- Fix 2: Drop and recreate RLS policy with WITH CHECK
DROP POLICY IF EXISTS "your policy name" ON your_table;
CREATE POLICY "users_own_your_table" ON your_table
FOR ALL
TO authenticated  
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

---

## 📋 TEMPLATE: Correct Upsert Pattern (Use This Every Time)

```javascript
async function saveToTable() {
  if (!currentBizId || !currentUser?.id) {
    console.error('No business or user selected');
    return;
  }

  const payload = {
    business_id: currentBizId,
    user_id: currentUser.id,
    // your fields here
    updated_at: new Date().toISOString()
  };

  console.log('[save] payload:', payload);

  const { data, error } = await sb
    .from('your_table')
    .upsert(payload, { onConflict: 'business_id' })
    .select()
    .single();

  console.log('[save] result:', data, error);

  if (error) {
    console.error('[save] failed:', error);
    // show error to user
    return;
  }

  // success
}
```

---

## 📋 TEMPLATE: Correct Load Pattern (Use This Every Time)

```javascript
async function loadFromTable() {
  if (!currentBizId) return;

  const { data, error } = await sb
    .from('your_table')
    .select('*')
    .eq('business_id', currentBizId)
    .single();

  console.log('[load] data:', data, 'error:', error);

  if (error && error.code !== 'PGRST116') {
    console.error('[load] failed:', error);
    return;
  }

  if (!data) {
    console.log('[load] no existing record');
    return;
  }

  // populate fields
  const fields = {
    'field-id-1': data.column1,
    'field-id-2': data.column2,
  };
  
  Object.entries(fields).forEach(([id, val]) => {
    const el = document.getElementById(id);
    if (el) el.value = val || '';
  });
}
```

---

## 🔑 KEY LESSONS LEARNED

1. Always add UNIQUE constraint before using onConflict in upsert
2. Always include WITH CHECK in RLS policies — USING alone blocks inserts
3. Always use TO authenticated not TO public on policies
4. Always chain .select() on upsert if you need the returned data
5. Always log payload AND result before and after every Supabase call
6. PGRST116 on load = data never saved (check the save first)
7. null error + null data on upsert = success (just no .select() chained)
8. Test upsert directly in browser console before debugging JS code
9. Test insert directly in Supabase SQL editor to rule out RLS issues
10. getUser() not getSession() for authenticated Supabase reads
