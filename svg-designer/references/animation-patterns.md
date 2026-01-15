# Animation Patterns

SVG animation patterns for loading states, transitions, and micro-interactions.

## Loading Spinners

### Rotating Circle Spinner

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50" width="50" height="50">
  <style>
    .spinner {
      animation: rotate 1s linear infinite;
      transform-origin: center;
    }
    @keyframes rotate {
      100% { transform: rotate(360deg); }
    }
  </style>
  
  <circle 
    class="spinner"
    cx="25" 
    cy="25" 
    r="20" 
    fill="none" 
    stroke="#6366F1" 
    stroke-width="4"
    stroke-linecap="round"
    stroke-dasharray="80, 200"
  />
</svg>
```

### Pulsing Dots

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 20" width="80" height="20">
  <style>
    .dot {
      animation: pulse 1.4s ease-in-out infinite;
    }
    .dot:nth-child(1) { animation-delay: 0s; }
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes pulse {
      0%, 80%, 100% { 
        transform: scale(0.6);
        opacity: 0.5;
      }
      40% { 
        transform: scale(1);
        opacity: 1;
      }
    }
  </style>
  
  <circle class="dot" cx="15" cy="10" r="6" fill="#6366F1"/>
  <circle class="dot" cx="40" cy="10" r="6" fill="#6366F1"/>
  <circle class="dot" cx="65" cy="10" r="6" fill="#6366F1"/>
</svg>
```

### Progress Ring

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <style>
    .progress-ring {
      transform: rotate(-90deg);
      transform-origin: center;
    }
    .progress-ring__circle {
      stroke-dasharray: 251.2; /* 2 * PI * 40 */
      stroke-dashoffset: 251.2;
      animation: progress 2s ease-out forwards;
    }
    @keyframes progress {
      to { stroke-dashoffset: 62.8; } /* 75% progress */
    }
  </style>
  
  <!-- Background track -->
  <circle 
    cx="50" 
    cy="50" 
    r="40" 
    fill="none" 
    stroke="#E5E7EB" 
    stroke-width="8"
  />
  
  <!-- Progress indicator -->
  <g class="progress-ring">
    <circle 
      class="progress-ring__circle"
      cx="50" 
      cy="50" 
      r="40" 
      fill="none" 
      stroke="#6366F1" 
      stroke-width="8"
      stroke-linecap="round"
    />
  </g>
  
  <!-- Percentage text -->
  <text 
    x="50" 
    y="55" 
    text-anchor="middle" 
    font-family="system-ui" 
    font-size="18" 
    font-weight="600"
    fill="#1F2937"
  >
    75%
  </text>
</svg>
```

### Morphing Shapes Loader

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="30" y="30" width="40" height="40" rx="4" fill="#6366F1">
    <animate 
      attributeName="rx" 
      values="4;20;4" 
      dur="1.5s" 
      repeatCount="indefinite"
    />
    <animate 
      attributeName="ry" 
      values="4;20;4" 
      dur="1.5s" 
      repeatCount="indefinite"
    />
    <animateTransform 
      attributeName="transform" 
      type="rotate" 
      values="0 50 50;180 50 50;360 50 50" 
      dur="1.5s" 
      repeatCount="indefinite"
    />
  </rect>
</svg>
```

### Bouncing Bars

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 40" width="50" height="40">
  <style>
    .bar {
      animation: bounce 1s ease-in-out infinite;
    }
    .bar:nth-child(1) { animation-delay: 0s; }
    .bar:nth-child(2) { animation-delay: 0.1s; }
    .bar:nth-child(3) { animation-delay: 0.2s; }
    .bar:nth-child(4) { animation-delay: 0.3s; }
    
    @keyframes bounce {
      0%, 100% { height: 10px; y: 15px; }
      50% { height: 30px; y: 5px; }
    }
  </style>
  
  <rect class="bar" x="5" y="15" width="6" height="10" rx="2" fill="#6366F1"/>
  <rect class="bar" x="16" y="15" width="6" height="10" rx="2" fill="#6366F1"/>
  <rect class="bar" x="27" y="15" width="6" height="10" rx="2" fill="#6366F1"/>
  <rect class="bar" x="38" y="15" width="6" height="10" rx="2" fill="#6366F1"/>
</svg>
```

---

## Micro-Interactions

### Checkbox Animation

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
  <style>
    .checkbox-bg {
      transition: fill 0.2s ease;
    }
    .checkbox-bg.checked {
      fill: #6366F1;
    }
    .checkmark {
      stroke-dasharray: 24;
      stroke-dashoffset: 24;
      transition: stroke-dashoffset 0.3s ease;
    }
    .checkmark.checked {
      stroke-dashoffset: 0;
    }
  </style>
  
  <!-- Background -->
  <rect 
    class="checkbox-bg checked" 
    x="2" y="2" 
    width="20" height="20" 
    rx="4" 
    fill="#6366F1"
  />
  
  <!-- Checkmark -->
  <path 
    class="checkmark checked"
    d="M6 12 L10 16 L18 8"
    fill="none"
    stroke="#FFFFFF"
    stroke-width="2.5"
    stroke-linecap="round"
    stroke-linejoin="round"
  />
</svg>
```

### Heart/Like Animation

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
  <style>
    .heart {
      fill: #E5E7EB;
      transform-origin: center;
      transition: fill 0.2s ease, transform 0.2s ease;
    }
    .heart:hover {
      fill: #F87171;
      transform: scale(1.1);
    }
    .heart.liked {
      fill: #EF4444;
      animation: heartbeat 0.4s ease;
    }
    @keyframes heartbeat {
      0% { transform: scale(1); }
      25% { transform: scale(1.2); }
      50% { transform: scale(0.95); }
      100% { transform: scale(1); }
    }
  </style>
  
  <path 
    class="heart"
    d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
  />
</svg>
```

### Toggle Switch

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 32" width="56" height="32">
  <style>
    .track {
      transition: fill 0.3s ease;
    }
    .track.on { fill: #6366F1; }
    .track.off { fill: #D1D5DB; }
    
    .thumb {
      transition: transform 0.3s ease;
    }
    .thumb.on { transform: translateX(24px); }
    .thumb.off { transform: translateX(0); }
  </style>
  
  <!-- Track -->
  <rect 
    class="track on" 
    x="0" y="0" 
    width="56" height="32" 
    rx="16"
  />
  
  <!-- Thumb -->
  <circle 
    class="thumb on" 
    cx="16" cy="16" r="12" 
    fill="#FFFFFF"
    filter="drop-shadow(0 1px 2px rgba(0,0,0,0.1))"
  />
</svg>
```

### Button Ripple Effect

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 40" width="120" height="40">
  <style>
    .ripple {
      transform-origin: center;
      animation: ripple 0.6s ease-out forwards;
    }
    @keyframes ripple {
      0% {
        transform: scale(0);
        opacity: 0.5;
      }
      100% {
        transform: scale(4);
        opacity: 0;
      }
    }
  </style>
  
  <!-- Button background -->
  <rect x="0" y="0" width="120" height="40" rx="8" fill="#6366F1"/>
  
  <!-- Ripple (triggered on click) -->
  <circle class="ripple" cx="60" cy="20" r="10" fill="#FFFFFF"/>
  
  <!-- Button text -->
  <text 
    x="60" y="25" 
    text-anchor="middle" 
    font-family="system-ui" 
    font-size="14" 
    font-weight="600"
    fill="#FFFFFF"
  >
    Click Me
  </text>
</svg>
```

---

## Transitions

### Draw-on Effect (Path Animation)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <style>
    .draw-on {
      stroke-dasharray: 300;
      stroke-dashoffset: 300;
      animation: draw 2s ease forwards;
    }
    @keyframes draw {
      to { stroke-dashoffset: 0; }
    }
  </style>
  
  <!-- Signature/logo path -->
  <path 
    class="draw-on"
    d="M20 80 Q30 20 50 50 T80 20"
    fill="none"
    stroke="#6366F1"
    stroke-width="4"
    stroke-linecap="round"
  />
</svg>
```

### Fade-in Stagger

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" width="200" height="100">
  <style>
    .fade-item {
      opacity: 0;
      animation: fadeIn 0.5s ease forwards;
    }
    .fade-item:nth-child(1) { animation-delay: 0s; }
    .fade-item:nth-child(2) { animation-delay: 0.1s; }
    .fade-item:nth-child(3) { animation-delay: 0.2s; }
    .fade-item:nth-child(4) { animation-delay: 0.3s; }
    
    @keyframes fadeIn {
      from { 
        opacity: 0;
        transform: translateY(10px);
      }
      to { 
        opacity: 1;
        transform: translateY(0);
      }
    }
  </style>
  
  <rect class="fade-item" x="10" y="20" width="40" height="60" rx="4" fill="#6366F1"/>
  <rect class="fade-item" x="60" y="20" width="40" height="60" rx="4" fill="#8B5CF6"/>
  <rect class="fade-item" x="110" y="20" width="40" height="60" rx="4" fill="#A78BFA"/>
  <rect class="fade-item" x="160" y="20" width="30" height="60" rx="4" fill="#C4B5FD"/>
</svg>
```

### Morph Between Shapes

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Play to Pause morph -->
  <path fill="#6366F1">
    <!-- Play triangle morphs to pause bars -->
    <animate 
      attributeName="d"
      dur="0.3s"
      fill="freeze"
      values="M30 20 L30 80 L80 50 Z;
              M25 20 L40 20 L40 80 L25 80 Z M60 20 L75 20 L75 80 L60 80 Z"
    />
  </path>
</svg>
```

---

## SMIL vs CSS Animations

### SMIL (Native SVG Animation)

```svg
<!-- Pros: No CSS, works everywhere SVG works -->
<!-- Cons: Deprecated in Chrome (still works), limited -->
<circle cx="50" cy="50" r="20" fill="#6366F1">
  <animate 
    attributeName="r" 
    values="20;25;20" 
    dur="1s" 
    repeatCount="indefinite"
  />
  <animate 
    attributeName="opacity" 
    values="1;0.5;1" 
    dur="1s" 
    repeatCount="indefinite"
  />
</circle>
```

### CSS Animation (Recommended)

```svg
<!-- Pros: Full animation control, consistent with web -->
<!-- Cons: Requires style block -->
<svg>
  <style>
    .animated { animation: pulse 1s infinite; }
    @keyframes pulse {
      0%, 100% { r: 20; opacity: 1; }
      50% { r: 25; opacity: 0.5; }
    }
  </style>
  <circle class="animated" cx="50" cy="50" r="20" fill="#6366F1"/>
</svg>
```

---

## Performance Tips

1. **Use `transform` over changing attributes**
   ```css
   /* Good - GPU accelerated */
   transform: translateX(10px);
   
   /* Avoid - causes reflow */
   cx: 60;
   ```

2. **Use `will-change` for complex animations**
   ```css
   .animated { will-change: transform, opacity; }
   ```

3. **Prefer CSS animations over SMIL**
   - Better browser support
   - More control
   - Easier to debug

4. **Minimize animated elements**
   - Animate groups, not individual paths
   - Use opacity/transform when possible

5. **Consider `prefers-reduced-motion`**
   ```css
   @media (prefers-reduced-motion: reduce) {
     .animated { animation: none; }
   }
   ```
