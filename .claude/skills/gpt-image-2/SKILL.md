# GPT Image 2 Ad Prompt Engineering Skill
# Based on Anil-matcha/Awesome-GPT-Image-2-API-Prompts

## Core Principle
GPT Image 2 rewards precise briefs over keyword chains.
Name the job. Define success. The model follows structure.

## Ad Image Prompt Formula
Use this exact structure for every ad image prompt:

[Product type] advertising photo, [service/product name],
location="[city, province]",
subject=[person description — age, gender, expression, what they're doing],
setting=[environment — specific, not generic],
lighting=[specific lighting — golden hour, soft window light, etc.],
text overlay: "[top line text]" at top in [font style],
headline: "[main headline]" in [size] [font style],
subtext: "[supporting text]" [smaller/beneath],
CTA: "[button text]" [position],
aesthetic=[3-5 specific style words],
color palette=[specific colors],
NOT=[3-5 specific exclusions],
aspect ratio [ratio], photorealistic editorial quality

## Text Rendering Rules
- Put exact text in quotes: "ST. CATHARINES SUMMER LAUNCH"
- Name placement explicitly: "at top", "centered", "bottom left"
- Specify font style: "elegant serif", "bold sans-serif", "small caps"
- Specify size hierarchy: "large headline", "smaller subtext", "tiny caption"
- GPT Image 2 renders text at ~99% accuracy when explicitly specified

## Beauty/Wellness Ad Prompts (for Stay Radiant and similar clients)

### Portrait with Text Overlay (primary ad format)
Product advertising photo, mobile [service] brand,
name="[Brand]", location="[City], Ontario",
subject=confident [age] woman, [expression], [what she's doing],
setting=[warm specific environment], [lighting],
text overlay: "[TOP LINE]" at top in small elegant caps white text,
headline: "[MAIN HEADLINE]" large elegant serif white,
subtext: "[SUPPORTING TEXT]" smaller serif below headline,
CTA button: "[CTA]" centered bottom with [color] background,
aesthetic=premium minimal feminine clean,
color palette=warm cream neutral tones soft gold accents,
NOT=clinical dental imagery, stock photo look, cheap coupon aesthetic,
aspect ratio 4:5, photorealistic

### Clean Background Product Shot
[Product/service] lifestyle flat lay,
warm cream linen background, premium beauty brand feel,
[specific items in shot], soft directional natural light,
text: "[HEADLINE]" top center in elegant serif,
brand name: "[Brand]" bottom center small caps,
aspect ratio 4:5, editorial product photography

## Key Rules
1. Always specify exact text in quotes
2. Always name text placement explicitly  
3. Always specify font style for each text element
4. Use "NOT=" to exclude unwanted elements
5. Specify aspect ratio always
6. End with "photorealistic" or "editorial photography quality"
7. Keep prompts under 400 words
8. No MidJourney syntax (no --ar, no --v flags)
