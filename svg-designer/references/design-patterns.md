# Design Patterns

SVG design patterns for logos, icons, and illustrations.

## Logo Patterns

### Pattern 1: Geometric Lettermark

```svg
<!-- Geometric "A" lettermark -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-labelledby="title">
  <title id="title">Apex Logo</title>
  
  <defs>
    <linearGradient id="brand-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366F1" />
      <stop offset="100%" stop-color="#4F46E5" />
    </linearGradient>
  </defs>
  
  <g id="logo">
    <!-- Triangle form creating "A" -->
    <path 
      d="M50 10 L90 90 L70 90 L60 70 L40 70 L30 90 L10 90 Z M50 35 L40 55 L60 55 Z"
      fill="url(#brand-gradient)"
      fill-rule="evenodd"
    />
  </g>
</svg>
```

**When to use**: Tech companies, startups, modern brands
**Key elements**: Sharp angles, mathematical precision, gradient adds depth

---

### Pattern 2: Abstract Symbol

```svg
<!-- Abstract flowing symbol -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-labelledby="title">
  <title id="title">Flow Logo</title>
  
  <defs>
    <linearGradient id="flow-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06B6D4" />
      <stop offset="50%" stop-color="#3B82F6" />
      <stop offset="100%" stop-color="#8B5CF6" />
    </linearGradient>
  </defs>
  
  <g id="logo">
    <!-- Flowing wave forms -->
    <path 
      d="M10 50 Q30 20 50 50 T90 50"
      fill="none"
      stroke="url(#flow-gradient)"
      stroke-width="8"
      stroke-linecap="round"
    />
    <path 
      d="M10 65 Q30 35 50 65 T90 65"
      fill="none"
      stroke="url(#flow-gradient)"
      stroke-width="6"
      stroke-linecap="round"
      opacity="0.6"
    />
  </g>
</svg>
```

**When to use**: Creative agencies, music/audio, fluid/dynamic brands
**Key elements**: Bezier curves, flowing motion, gradient progression

---

### Pattern 3: Combination Mark (Icon + Wordmark)

```svg
<!-- Icon with wordmark -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60" role="img" aria-labelledby="title">
  <title id="title">Pulse Brand Logo</title>
  
  <g id="logo">
    <!-- Icon: Stylized pulse/heartbeat -->
    <g id="icon">
      <circle cx="30" cy="30" r="25" fill="#EF4444" opacity="0.1"/>
      <path 
        d="M15 30 L22 30 L26 20 L30 40 L34 25 L38 30 L45 30"
        fill="none"
        stroke="#EF4444"
        stroke-width="3"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </g>
    
    <!-- Wordmark -->
    <g id="wordmark">
      <text 
        x="65" 
        y="38" 
        font-family="system-ui, -apple-system, sans-serif"
        font-size="28"
        font-weight="600"
        fill="#1F2937"
      >
        Pulse
      </text>
    </g>
  </g>
</svg>
```

**When to use**: Health tech, fitness, monitoring services
**Key elements**: Recognizable icon, clean typography, balanced spacing

---

### Pattern 4: Negative Space

```svg
<!-- Negative space logo (arrow in "E") -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-labelledby="title">
  <title id="title">Evolve Logo</title>
  
  <g id="logo">
    <rect x="10" y="10" width="80" height="80" rx="8" fill="#1F2937"/>
    
    <!-- E shape with arrow negative space -->
    <path 
      d="M25 25 L65 25 L65 35 L35 35 L35 45 L55 45 L55 55 L35 55 L35 65 L65 65 L65 75 L25 75 Z"
      fill="#FFFFFF"
    />
    
    <!-- Arrow pointing right (negative space creates forward motion) -->
    <path 
      d="M55 45 L75 50 L55 55 Z"
      fill="#1F2937"
    />
  </g>
</svg>
```

**When to use**: Brands emphasizing progress, transformation, clever messaging
**Key elements**: Hidden meaning, memorable reveal, sophisticated design

---

### Pattern 5: Typographic Logo

```svg
<!-- Custom typography logo -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50" role="img" aria-labelledby="title">
  <title id="title">Mono Studio</title>
  
  <g id="logo">
    <!-- Custom letterforms -->
    <text 
      x="10" 
      y="38" 
      font-family="ui-monospace, monospace"
      font-size="32"
      font-weight="700"
      letter-spacing="4"
      fill="#000000"
    >
      MONO
    </text>
    
    <!-- Accent line -->
    <rect x="10" y="44" width="110" height="2" fill="#6366F1"/>
    
    <text 
      x="130" 
      y="38" 
      font-family="ui-monospace, monospace"
      font-size="32"
      font-weight="300"
      letter-spacing="2"
      fill="#6B7280"
    >
      studio
    </text>
  </g>
</svg>
```

**When to use**: Design studios, personal brands, luxury
**Key elements**: Typography as hero, weight contrast, minimal decoration

---

## Icon Patterns

### Outline Style (Stroke-based)

```svg
<!-- Settings icon - outline -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="3"/>
  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
</svg>
```

### Filled Style

```svg
<!-- Home icon - filled -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 2.1L1 12h3v9h7v-6h2v6h7v-9h3L12 2.1z"/>
</svg>
```

### Duotone Style

```svg
<!-- Folder icon - duotone -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <!-- Background layer (lighter) -->
  <path 
    d="M3 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6z"
    fill="currentColor"
    opacity="0.3"
  />
  <!-- Foreground layer (darker) -->
  <path 
    d="M3 8h18v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8z"
    fill="currentColor"
  />
</svg>
```

---

## Illustration Patterns

### Spot Illustration (Simple Scene)

```svg
<!-- Empty state illustration -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 150" role="img" aria-labelledby="title desc">
  <title id="title">No Results</title>
  <desc id="desc">Illustration of an empty box with a magnifying glass</desc>
  
  <defs>
    <linearGradient id="box-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F3F4F6"/>
      <stop offset="100%" stop-color="#E5E7EB"/>
    </linearGradient>
  </defs>
  
  <g id="illustration">
    <!-- Shadow -->
    <ellipse cx="100" cy="130" rx="60" ry="10" fill="#E5E7EB"/>
    
    <!-- Box -->
    <g id="box">
      <!-- Front face -->
      <path d="M50 60 L100 80 L150 60 L150 110 L100 130 L50 110 Z" fill="url(#box-gradient)"/>
      <!-- Top face -->
      <path d="M50 60 L100 40 L150 60 L100 80 Z" fill="#F9FAFB"/>
      <!-- Side edge -->
      <path d="M100 80 L100 130" stroke="#D1D5DB" stroke-width="1"/>
    </g>
    
    <!-- Magnifying glass -->
    <g id="magnifier">
      <circle cx="130" cy="45" r="18" fill="none" stroke="#9CA3AF" stroke-width="4"/>
      <line x1="143" y1="58" x2="158" y2="73" stroke="#9CA3AF" stroke-width="4" stroke-linecap="round"/>
      <!-- Glare -->
      <path d="M120 38 Q125 33 130 38" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
    </g>
  </g>
</svg>
```

### Isometric Pattern

```svg
<!-- Isometric cube/building block -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <g id="isometric-cube">
    <!-- Top face -->
    <path d="M50 20 L80 35 L50 50 L20 35 Z" fill="#6366F1"/>
    <!-- Left face -->
    <path d="M20 35 L50 50 L50 80 L20 65 Z" fill="#4F46E5"/>
    <!-- Right face -->
    <path d="M50 50 L80 35 L80 65 L50 80 Z" fill="#818CF8"/>
  </g>
</svg>
```

---

## Badge/Seal Patterns

### Circular Badge

```svg
<!-- Trust badge -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="badge-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
  </defs>
  
  <g id="badge">
    <!-- Outer ring -->
    <circle cx="50" cy="50" r="45" fill="none" stroke="url(#badge-gradient)" stroke-width="4"/>
    
    <!-- Inner circle -->
    <circle cx="50" cy="50" r="35" fill="url(#badge-gradient)"/>
    
    <!-- Checkmark -->
    <path 
      d="M35 50 L45 60 L65 40"
      fill="none"
      stroke="#FFFFFF"
      stroke-width="5"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
    
    <!-- Text on path -->
    <path id="textPath" d="M15 50 A35 35 0 1 1 85 50" fill="none"/>
    <text font-size="8" fill="#059669" font-weight="600">
      <textPath href="#textPath" startOffset="15%">VERIFIED • TRUSTED</textPath>
    </text>
  </g>
</svg>
```

---

## Responsive Logo Pattern

```svg
<!-- Logo that adapts: full version vs icon only -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50">
  <style>
    /* Icon always visible */
    #icon { display: block; }
    
    /* Wordmark hidden on small screens */
    @media (max-width: 400px) {
      #wordmark { display: none; }
    }
  </style>
  
  <g id="logo">
    <g id="icon">
      <circle cx="25" cy="25" r="20" fill="#6366F1"/>
      <path d="M18 25 L23 30 L32 20" stroke="#FFF" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    
    <g id="wordmark">
      <text x="55" y="32" font-family="system-ui" font-size="24" font-weight="600" fill="#1F2937">
        BrandName
      </text>
    </g>
  </g>
</svg>
```
