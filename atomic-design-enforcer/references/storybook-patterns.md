# Storybook Patterns and Examples

Complete examples for Storybook stories at each atomic level.

## Atoms - Button Example

```javascript
// Button.stories.jsx
import { Button } from './Button';

export default {
  title: 'Atoms/Button',
  component: Button,
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'tertiary', 'danger'],
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
    },
    disabled: { control: 'boolean' },
  },
};

// Default story
export const Primary = {
  args: {
    children: 'Click me',
    variant: 'primary',
  },
};

// All variants
export const AllVariants = () => (
  <div style={{ display: 'flex', gap: '1rem' }}>
    <Button variant="primary">Primary</Button>
    <Button variant="secondary">Secondary</Button>
    <Button variant="tertiary">Tertiary</Button>
    <Button variant="danger">Danger</Button>
  </div>
);

// All sizes
export const AllSizes = () => (
  <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
    <Button size="small">Small</Button>
    <Button size="medium">Medium</Button>
    <Button size="large">Large</Button>
  </div>
);

// States
export const Disabled = {
  args: {
    children: 'Disabled',
    disabled: true,
  },
};

export const WithIcon = {
  args: {
    children: (
      <>
        <Icon name="check" /> Save
      </>
    ),
  },
};
```

**Minimum requirement**: 5+ stories covering default + all variants + states

## Molecules - SearchField Example

```javascript
// SearchField.stories.jsx
export default {
  title: 'Molecules/SearchField',
  component: SearchField,
};

export const Default = {
  args: {
    placeholder: 'Search...',
  },
};

export const WithValue = {
  args: {
    placeholder: 'Search...',
    value: 'Current search term',
  },
};

export const Loading = {
  args: {
    placeholder: 'Search...',
    isLoading: true,
  },
};

export const WithError = {
  args: {
    placeholder: 'Search...',
    error: 'Search failed. Please try again.',
  },
};

export const Interactive = () => {
  const [value, setValue] = React.useState('');
  return (
    <SearchField
      value={value}
      onChange={(e) => setValue(e.target.value)}
      onSearch={() => alert(`Searching for: ${value}`)}
      placeholder="Type and click search..."
    />
  );
};
```

**Minimum requirement**: 6+ stories covering default + variants + states + interactive behavior

## Organisms - ProductCard Example

```javascript
// ProductCard.stories.jsx
export default {
  title: 'Organisms/ProductCard',
  component: ProductCard,
  parameters: {
    layout: 'padded',
  },
};

const mockProduct = {
  id: '1',
  name: 'Wireless Headphones',
  category: 'Electronics',
  price: 99.99,
  currency: 'USD',
  rating: 4.5,
  reviewCount: 127,
  image: 'https://via.placeholder.com/300x300',
};

export const Default = {
  args: {
    product: mockProduct,
    onAddToCart: (id) => console.log('Add to cart:', id),
    onViewDetails: (id) => console.log('View details:', id),
  },
};

export const OutOfStock = {
  args: {
    product: { ...mockProduct, inStock: false },
    onAddToCart: (id) => console.log('Add to cart:', id),
    onViewDetails: (id) => console.log('View details:', id),
  },
};

export const OnSale = {
  args: {
    product: {
      ...mockProduct,
      price: 79.99,
      originalPrice: 99.99,
      discount: 20,
    },
    onAddToCart: (id) => console.log('Add to cart:', id),
    onViewDetails: (id) => console.log('View details:', id),
  },
};

export const LongProductName = {
  args: {
    product: {
      ...mockProduct,
      name: 'Premium Wireless Noise-Cancelling Over-Ear Headphones with Extended Battery Life',
    },
    onAddToCart: (id) => console.log('Add to cart:', id),
    onViewDetails: (id) => console.log('View details:', id),
  },
};

export const NoReviews = {
  args: {
    product: {
      ...mockProduct,
      rating: 0,
      reviewCount: 0,
    },
    onAddToCart: (id) => console.log('Add to cart:', id),
    onViewDetails: (id) => console.log('View details:', id),
  },
};

// Responsive behavior
export const MobileView = {
  args: {
    product: mockProduct,
    onAddToCart: (id) => console.log('Add to cart:', id),
    onViewDetails: (id) => console.log('View details:', id),
  },
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};
```

**Minimum requirement**: 8+ stories covering default + empty + error + loading + edge cases + responsive

## Templates - DashboardTemplate Example

```javascript
// DashboardTemplate.stories.jsx
export default {
  title: 'Templates/DashboardTemplate',
  component: DashboardTemplate,
  parameters: {
    layout: 'fullscreen',
  },
};

export const Default = {
  args: {
    header: <div style={{ padding: '1rem', background: '#f0f0f0' }}>Header Content</div>,
    sidebar: <div style={{ padding: '1rem', background: '#e0e0e0' }}>Sidebar Content</div>,
    mainContent: <div style={{ padding: '2rem', background: '#fff' }}>Main Content</div>,
    footer: <div style={{ padding: '1rem', background: '#f0f0f0' }}>Footer Content</div>,
  },
};

export const WithoutSidebar = {
  args: {
    header: <div style={{ padding: '1rem', background: '#f0f0f0' }}>Header Content</div>,
    mainContent: <div style={{ padding: '2rem', background: '#fff' }}>Main Content</div>,
    footer: <div style={{ padding: '1rem', background: '#f0f0f0' }}>Footer Content</div>,
  },
};

export const MobileLayout = {
  args: {
    header: <div style={{ padding: '1rem', background: '#f0f0f0' }}>Header</div>,
    sidebar: <div style={{ padding: '1rem', background: '#e0e0e0' }}>Sidebar (collapsed)</div>,
    mainContent: <div style={{ padding: '1rem', background: '#fff' }}>Main</div>,
    footer: <div style={{ padding: '1rem', background: '#f0f0f0' }}>Footer</div>,
  },
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};
```

**Minimum requirement**: 4+ stories showing layout flexibility and responsive behavior

## Interaction Testing

Use Storybook's play functions to test interactions:

```javascript
// SearchField.stories.jsx
import { within, userEvent, expect } from '@storybook/test';

export const UserTypesAndSearches = {
  args: {
    placeholder: 'Search products...',
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Find the input
    const input = canvas.getByPlaceholderText('Search products...');

    // Type into input
    await userEvent.type(input, 'wireless headphones');

    // Verify value
    await expect(input).toHaveValue('wireless headphones');

    // Click search button
    const searchButton = canvas.getByRole('button', { name: /search/i });
    await userEvent.click(searchButton);
  },
};

export const ShowsErrorMessage = {
  args: {
    placeholder: 'Search...',
    error: 'Search failed',
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Verify error is displayed
    const error = canvas.getByText('Search failed');
    await expect(error).toBeInTheDocument();
  },
};
```

## MDX Documentation

For complex organisms and templates:

```mdx
{/* ProductCard.mdx */}
import { Meta, Canvas, Story, Controls } from '@storybook/blocks';
import * as ProductCardStories from './ProductCard.stories';

<Meta of={ProductCardStories} />

# ProductCard

Displays product information with image, details, pricing, and actions.

## Usage

This organism combines multiple molecules and atoms to create a self-contained product display unit.

<Canvas of={ProductCardStories.Default} />

## Props

<Controls />

## Variants

### Out of Stock
<Canvas of={ProductCardStories.OutOfStock} />

### On Sale
<Canvas of={ProductCardStories.OnSale} />

## Guidelines

- Always provide product image
- Handle missing data gracefully
- Ensure click targets are minimum 44px
- Support keyboard navigation
```

## Storybook Configuration

### Main Configuration

```javascript
// .storybook/main.js
export default {
  stories: [
    '../src/components/**/*.stories.@(js|jsx|ts|tsx|mdx)',
  ],
  addons: [
    '@storybook/addon-essentials',      // Controls, actions, docs
    '@storybook/addon-interactions',    // Play function testing
    '@storybook/addon-a11y',           // Accessibility testing
    '@storybook/addon-viewport',        // Responsive testing
    '@chromatic-com/storybook',        // Visual regression
  ],
  framework: {
    name: '@storybook/react-vite',     // Or webpack
    options: {},
  },
};
```

### Preview Configuration

```javascript
// .storybook/preview.js
import React from 'react';
import { ThemeProvider } from '../src/theme';

export const decorators = [
  (Story) => (
    <ThemeProvider>
      <Story />
    </ThemeProvider>
  ),
];

export const parameters = {
  actions: { argTypesRegex: '^on[A-Z].*' },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
  viewport: {
    viewports: {
      mobile1: { name: 'Small Mobile', styles: { width: '375px', height: '667px' } },
      tablet: { name: 'Tablet', styles: { width: '768px', height: '1024px' } },
      desktop: { name: 'Desktop', styles: { width: '1280px', height: '800px' } },
    },
  },
};
```

## Story Anti-Patterns

### FORBIDDEN Practices

**Stories with hard-coded business logic:**
```javascript
// WRONG
export const UserProfile = {
  args: {
    userId: 123,
  },
  render: (args) => {
    const user = fetchUser(args.userId);  // NO API calls
    return <UserProfile user={user} />;
  },
};

// CORRECT
export const UserProfile = {
  args: {
    user: {
      id: 123,
      name: 'John Doe',
      email: 'john@example.com',
    },
  },
};
```

**Stories that violate atomic principles:**
```javascript
// WRONG - Atom fetching data
export const ButtonWithUserName = () => {
  const user = useCurrentUser();  // NO
  return <Button>{user.name}</Button>;
};

// CORRECT - Atom receives data as props
export const ButtonWithCustomText = {
  args: {
    children: 'John Doe',
  },
};
```
