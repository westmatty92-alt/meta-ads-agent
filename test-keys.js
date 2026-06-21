import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const SUPA_URL = 'https://ytumpmtkxkhhehmvljoy.supabase.co';
const SUPA_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl0dW1wbXRreGtoaGVobXZsam95Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE0MjgxMDEsImV4cCI6MjA5NzAwNDEwMX0.0CHSJ1iXW8e8q49cdgte80VrmDgX_COejMRVIRMxi9I';
const USER_ID = 'ceaa4f10-63c0-4e11-8780-9cf359bf51bc';

const sb = createClient(SUPA_URL, SUPA_KEY);

const { data, error } = await sb
  .from('user_keys')
  .select('*')
  .eq('user_id', USER_ID)
  .single();

console.log('error:', error);
console.log('data:', JSON.stringify(data, null, 2));
