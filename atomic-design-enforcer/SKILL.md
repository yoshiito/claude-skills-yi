---
name: atomic-design-enforcer
description: Militant enforcement of atomic design principles, component modularity, and Storybook documentation for frontend development. Use when building React components, creating component libraries, structuring frontend applications, refactoring component hierarchies, or ensuring comprehensive component documentation. Enforces strict 5-tier hierarchy (Atoms→Molecules→Organisms→Templates→Pages), single responsibility, composition patterns, mandatory Storybook stories with interaction tests, and systematic architecture with zero compromise.
---

# Atomic Design Enforcer

Enforce atomic design principles and modular architecture with zero compromise. This skill mandates strict adherence to component hierarchy, clear separation of concerns, and systematic code organization. Every component must justify its place in the atomic hierarchy and maintain single responsibility.

## Usage Notification

**REQUIRED**: When this skill is triggered, immediately state: "⚛️ Using Frontend Developer skill - enforcing atomic design principles and strict modularity."

This notification must appear at the start of the response before any development guidance.

## Atomic Design Hierarchy

**MANDATORY STRUCTURE**: All components must fit into one of these five categories. No exceptions.

### 1. Atoms
**Definition**: The fundamental building blocks. Smallest functional units that cannot be broken down further without losing meaning.

**Examples**:
- Buttons (primary, secondary, tertiary variants)
- Input fields (text, number, email, password)
- Labels, icons, badges
- Typography components (Heading, Paragraph, Caption)
- Form elements (Checkbox, Radio, Toggle)

**Rules**:
- Atoms receive primitive props only (strings, numbers, booleans)
- No business logic, only presentation logic
- No internal state beyond basic UI state (hover, focus, disabled)
- No API calls or data fetching
- Maximum 100 lines of code
- Must be fully testable in isolation
- Must have clear prop types/interfaces

**Structure**:
```javascript
// ✓ CORRECT: Pure, single-purpose atom
const Button = ({ variant, size, disabled, children, onClick }) => {
  return (
    <button 
      className={`btn btn--${variant} btn--${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};

// ✗ WRONG: Business logic in atom
const Button = ({ userId, onClick }) => {
  const user = fetchUser(userId); // NO - atoms don't fetch data
  return <button onClick={onClick}>{user.name}</button>;
};
```

### 2. Molecules
**Definition**: Simple combinations of atoms functioning together as a unit. Still relatively simple, focused on a single task.

**Examples**:
- Search input (input field + icon + button)
- Form field (label + input + error message)
- Card header (title + subtitle + icon)
- Navigation item (icon + label + badge)
- List item (checkbox + text + action button)

**Rules**:
- Combine 2-5 atoms into meaningful groups
- Accept props that configure composed atoms
- May contain simple interaction logic (form validation, toggle states)
- No complex business logic or data transformation
- No API calls or data fetching
- Maximum 150 lines of code
- Must be reusable across different contexts

**Structure**:
```javascript
// ✓ CORRECT: Focused molecule with clear purpose
const SearchField = ({ placeholder, value, onChange, onSearch }) => {
  return (
    <div className="search-field">
      <Icon name="search" />
      <Input 
        type="text"
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
      <Button variant="primary" size="small" onClick={onSearch}>
        Search
      </Button>
    </div>
  );
};

// ✗ WRONG: Too complex for molecule
const SearchField = ({ endpoint, filters, onResults }) => {
  const results = await fetchSearchResults(endpoint, filters); // NO
  return <div>...</div>;
};
```

### 3. Organisms
**Definition**: Complex components combining molecules and atoms into distinct interface sections. Represent relatively self-contained portions of an interface.

**Examples**:
- Navigation bars (logo + nav items + user menu + search)
- Data tables (column headers + rows + pagination + filters)
- Product cards (image + title + price + rating + actions)
- Forms (multiple form fields + validation + submit buttons)
- Comment sections (comment list + reply forms + user avatars)

**Rules**:
- Compose multiple molecules and atoms
- May contain complex interaction logic and local state
- Can manage data fetching for their specific domain
- Should remain context-independent where possible
- Maximum 300 lines of code
- Must be independently functional
- Clear interface for data input/output

**Structure**:
```javascript
// ✓ CORRECT: Self-contained organism with clear boundaries
const ProductCard = ({ product, onAddToCart, onViewDetails }) => {
  const [isFavorite, setIsFavorite] = useState(false);
  
  return (
    <Card elevation={2}>
      <CardImage src={product.image} alt={product.name} />
      <CardHeader title={product.name} subtitle={product.category} />
      <CardContent>
        <Price amount={product.price} currency={product.currency} />
        <Rating value={product.rating} reviews={product.reviewCount} />
      </CardContent>
      <CardActions>
        <IconButton 
          icon="favorite" 
          active={isFavorite}
          onClick={() => setIsFavorite(!isFavorite)} 
        />
        <Button variant="secondary" onClick={() => onViewDetails(product.id)}>
          Details
        </Button>
        <Button variant="primary" onClick={() => onAddToCart(product.id)}>
          Add to Cart
        </Button>
      </CardActions>
    </Card>
  );
};

// ✗ WRONG: Too much business logic
const ProductCard = ({ productId }) => {
  const product = useProductDetails(productId);
  const cart = useCart();
  const favorites = useFavorites();
  const recommendations = useRecommendations(productId);
  // NO - this is template territory, too much data orchestration
};
```

### 4. Templates
**Definition**: Page-level compositions that arrange organisms into layouts. Define structure and placement but remain content-agnostic.

**Examples**:
- Dashboard layout (header + sidebar + main content + footer)
- Blog post template (header + article content + sidebar + comments)
- E-commerce product page (breadcrumbs + product section + recommendations + footer)
- Settings page (tabs + form sections + action bar)

**Rules**:
- Define page structure and organism placement
- Accept content as props/children
- No specific content, only layout and structure
- May include responsive behavior and layout logic
- Maximum 250 lines of code (structural, not content)
- Should be reusable across similar page types

**Structure**:
```javascript
// ✓ CORRECT: Content-agnostic template
const DashboardTemplate = ({ 
  header, 
  sidebar, 
  mainContent, 
  footer 
}) => {
  return (
    <div className="dashboard-layout">
      <header className="dashboard-layout__header">
        {header}
      </header>
      <div className="dashboard-layout__body">
        <aside className="dashboard-layout__sidebar">
          {sidebar}
        </aside>
        <main className="dashboard-layout__content">
          {mainContent}
        </main>
      </div>
      <footer className="dashboard-layout__footer">
        {footer}
      </footer>
    </div>
  );
};

// ✗ WRONG: Template with specific content
const DashboardTemplate = () => {
  return (
    <div>
      <Header title="My Dashboard" /> {/* NO - too specific */}
      <Sidebar items={menuItems} /> {/* NO - content in template */}
    </div>
  );
};
```

### 5. Pages
**Definition**: Specific instances of templates with real content, data fetching, and business logic. The final assembled interfaces users interact with.

**Examples**:
- Home page
- User profile page
- Product details page
- Checkout page
- Admin dashboard

**Rules**:
- Use templates for structure
- Handle data fetching and state management
- Implement page-specific business logic
- Connect to stores/contexts as needed
- No line limit (but extract complexity into organisms)
- Should be route/navigation targets

**Structure**:
```javascript
// ✓ CORRECT: Page composes template with real data
const ProductDetailsPage = ({ productId }) => {
  const { data: product, loading, error } = useProduct(productId);
  const recommendations = useRecommendations(productId);
  const cart = useCart();
  
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  
  return (
    <ProductPageTemplate
      header={<SiteHeader />}
      breadcrumbs={<Breadcrumbs items={getBreadcrumbs(product)} />}
      productSection={
        <ProductDetailsOrganism 
          product={product}
          onAddToCart={cart.add}
        />
      }
      recommendations={
        <RecommendationsOrganism products={recommendations} />
      }
      footer={<SiteFooter />}
    />
  );
};
```

## Component Organization

**MANDATORY DIRECTORY STRUCTURE**:

```
src/
├── components/
│   ├── atoms/
│   │   ├── Button/
│   │   │   ├── Button.jsx
│   │   │   ├── Button.module.css
│   │   │   ├── Button.test.jsx
│   │   │   └── index.js
│   │   ├── Input/
│   │   └── Icon/
│   ├── molecules/
│   │   ├── SearchField/
│   │   ├── FormField/
│   │   └── NavItem/
│   ├── organisms/
│   │   ├── Header/
│   │   ├── ProductCard/
│   │   └── CommentSection/
│   ├── templates/
│   │   ├── DashboardTemplate/
│   │   └── ArticleTemplate/
│   └── pages/
│       ├── HomePage/
│       └── ProductPage/
├── hooks/
├── utils/
├── services/
└── stores/
```

**Each component directory must contain**:
- Component file (`.jsx`, `.tsx`)
- Styles (`.module.css`, `.scss`, or styled-components)
- Tests (`.test.jsx`, `.spec.jsx`)
- Index file for clean exports

## Storybook Requirements

**MANDATORY**: Every component must have complete Storybook stories before it's considered production-ready. Stories are not optional documentation - they're proof that your component works in isolation and adheres to atomic design principles.

### Story Requirements by Atomic Level

#### Atoms
**Required stories**:
- Default story showing the basic variant
- All visual variants (primary, secondary, disabled, error states, etc.)
- All size variants (small, medium, large)
- Interactive states (hover, focus, active, disabled)

**Example structure**:
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

#### Molecules
**Required stories**:
- Default story with typical usage
- All configuration variants
- Different data states (empty, single item, multiple items)
- Error states and validation scenarios
- Edge cases (long text, missing data, etc.)

**Example structure**:
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

#### Organisms
**Required stories**:
- Default story with realistic mock data
- Empty state
- Loading state
- Error state
- Populated state with various data scenarios
- Interactive behaviors with actions logging
- Responsive behavior at different viewport sizes

**Example structure**:
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

#### Templates
**Required stories**:
- Default layout with placeholder content
- Different content density scenarios (sparse, typical, dense)
- Responsive behavior at all breakpoints
- Different content combinations

**Example structure**:
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

#### Pages
**Pages generally don't need stories** since they're specific instances with real data and business logic. However, if creating stories for development purposes:
- Use MSW (Mock Service Worker) for API mocking
- Show different data loading states
- Document the full page flow

### Story Structure Standards

**MANDATORY naming conventions**:
```
components/
└── atoms/
    └── Button/
        ├── Button.jsx
        ├── Button.module.css
        ├── Button.stories.jsx    ← Stories file
        ├── Button.test.jsx
        └── index.js
```

**Story file structure**:
```javascript
import { ComponentName } from './ComponentName';

// 1. Default export with metadata
export default {
  title: 'AtomicLevel/ComponentName',  // Follow hierarchy
  component: ComponentName,
  tags: ['autodocs'],                  // Enable auto-documentation
  argTypes: {
    // Define controls for interactive props
  },
  parameters: {
    // Component-level parameters
  },
};

// 2. Named exports for each story
export const StoryName = {
  args: {
    // Story-specific props
  },
};

// 3. Or template pattern for complex stories
const Template = (args) => <ComponentName {...args} />;
export const AnotherStory = Template.bind({});
AnotherStory.args = { /* props */ };
```

**Story titles must follow atomic hierarchy**:
- `Atoms/ComponentName`
- `Molecules/ComponentName`
- `Organisms/ComponentName`
- `Templates/TemplateName`

This creates a clear Storybook navigation matching your file structure.

### Documentation Requirements

**MDX Documentation**: Complex organisms and templates must include MDX docs:

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

**Required documentation**:
- Component purpose and usage
- When to use vs alternatives
- Props documentation (auto-generated via Controls)
- Visual examples of all variants
- Accessibility notes
- Related components

### Interaction Testing

**MANDATORY for interactive components**: Use Storybook's play functions to test interactions:

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

**Requirements**:
- Every interactive molecule must have play function tests
- Test user interactions (click, type, focus, etc.)
- Verify state changes
- Test error conditions
- Test edge cases

### Visual Regression Testing

Integrate Storybook with visual regression tools:

```javascript
// .storybook/main.js
export default {
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@chromatic-com/storybook',  // For visual regression
  ],
};
```

**Requirements**:
- Run visual tests on every PR
- Approve intentional visual changes
- Flag unintended regressions
- Test across browsers (Chrome, Firefox, Safari)

### Storybook Configuration

**Mandatory addons**:
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

**Global decorators** for consistent story rendering:
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

### Storybook Anti-Patterns

**FORBIDDEN practices**:

❌ **Missing stories for components**: Every component must have stories. No exceptions.

❌ **Stories with hard-coded business logic**:
```javascript
// WRONG
export const UserProfile = {
  args: {
    userId: 123,  // Don't fetch real data in stories
  },
  render: (args) => {
    const user = fetchUser(args.userId);  // NO API calls
    return <UserProfile user={user} />;
  },
};

// CORRECT
export const UserProfile = {
  args: {
    user: {  // Use mock data
      id: 123,
      name: 'John Doe',
      email: 'john@example.com',
    },
  },
};
```

❌ **Incomplete variant coverage**: If your component has 5 variants, you need stories for all 5.

❌ **Stories that violate atomic principles**:
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

❌ **Mixing story levels**: Don't put organism stories in the Atoms section or vice versa.

❌ **Stories without interactions for interactive components**: If it's clickable, hoverable, or changeable, it needs interaction tests.

❌ **Undocumented complex organisms**: Organisms with 10+ props need MDX documentation.

### Story Checklist

Before considering stories complete:

**Structure**:
- [ ] Story file in same directory as component
- [ ] Follows naming convention (ComponentName.stories.jsx)
- [ ] Title matches atomic hierarchy (Atoms/Molecules/Organisms/Templates)
- [ ] Default export with proper metadata

**Coverage**:
- [ ] Default story exists
- [ ] All variants covered
- [ ] All states covered (loading, error, empty, success)
- [ ] Edge cases covered (long text, missing data, etc.)
- [ ] Responsive behavior tested (mobile, tablet, desktop)
- [ ] Meets minimum story count for atomic level

**Interactivity**:
- [ ] Interactive components have play function tests
- [ ] User interactions are tested
- [ ] State changes are verified
- [ ] Error conditions are tested

**Documentation**:
- [ ] ArgTypes defined for all configurable props
- [ ] Complex organisms have MDX documentation
- [ ] Usage guidelines documented
- [ ] Related components referenced

**Quality**:
- [ ] Stories use mock data, not real API calls
- [ ] No business logic in stories
- [ ] Stories are independent (can run in any order)
- [ ] Accessibility tested via a11y addon
- [ ] Visual regression tests passing

## Modularity Rules

### 1. Single Responsibility
Each component does ONE thing well. If a component has multiple concerns, split it.

```javascript
// ✗ WRONG: Multiple responsibilities
const UserWidget = () => {
  return (
    <div>
      <img src={user.avatar} /> {/* Avatar display */}
      <h3>{user.name}</h3> {/* Name display */}
      <button onClick={logout}>Logout</button> {/* Action */}
      <ul>{notifications.map(n => <li>{n}</li>)}</ul> {/* Notifications */}
    </div>
  );
};

// ✓ CORRECT: Separated concerns
const UserAvatar = ({ src, alt }) => <img src={src} alt={alt} />;
const UserName = ({ name }) => <h3>{name}</h3>;
const LogoutButton = ({ onLogout }) => <button onClick={onLogout}>Logout</button>;
const NotificationList = ({ notifications }) => (
  <ul>{notifications.map(n => <NotificationItem key={n.id} {...n} />)}</ul>
);

const UserWidget = ({ user, notifications, onLogout }) => (
  <div>
    <UserAvatar src={user.avatar} alt={user.name} />
    <UserName name={user.name} />
    <LogoutButton onLogout={onLogout} />
    <NotificationList notifications={notifications} />
  </div>
);
```

### 2. Composition Over Inheritance
Build complexity through composition, never through class inheritance or component extension.

```javascript
// ✗ WRONG: Inheritance pattern
class SpecialButton extends Button {
  render() {
    return <button className="special">{this.props.children}</button>;
  }
}

// ✓ CORRECT: Composition pattern
const IconButton = ({ icon, children, ...buttonProps }) => (
  <Button {...buttonProps}>
    <Icon name={icon} />
    {children}
  </Button>
);
```

### 3. Prop Drilling vs Context
Avoid deep prop drilling. Use context/state management for data that crosses 3+ levels.

```javascript
// ✗ WRONG: Excessive prop drilling
<App>
  <Layout theme={theme}>
    <Header theme={theme}>
      <Nav theme={theme}>
        <NavItem theme={theme} /> {/* 4 levels deep */}
      </Nav>
    </Header>
  </Layout>
</App>

// ✓ CORRECT: Context for cross-cutting concerns
<ThemeProvider value={theme}>
  <App>
    <Layout>
      <Header>
        <Nav>
          <NavItem /> {/* Accesses theme from context */}
        </Nav>
      </Header>
    </Layout>
  </App>
</ThemeProvider>
```

### 4. Explicit Dependencies
Components declare all dependencies explicitly through props. No hidden dependencies or global access.

```javascript
// ✗ WRONG: Hidden global dependency
const UserProfile = () => {
  const user = window.currentUser; // NO - hidden dependency
  return <div>{user.name}</div>;
};

// ✓ CORRECT: Explicit dependency
const UserProfile = ({ user }) => {
  return <div>{user.name}</div>;
};
```

### 5. Separation of Logic and Presentation
Business logic lives in custom hooks or services. Components handle presentation only.

```javascript
// ✗ WRONG: Mixed logic and presentation
const UserList = () => {
  const [users, setUsers] = useState([]);
  
  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => {
        const filtered = data.filter(u => u.active);
        const sorted = filtered.sort((a, b) => a.name.localeCompare(b.name));
        setUsers(sorted);
      });
  }, []);
  
  return <ul>{users.map(u => <li>{u.name}</li>)}</ul>;
};

// ✓ CORRECT: Separated concerns
const useUsers = () => {
  const [users, setUsers] = useState([]);
  
  useEffect(() => {
    fetchUsers().then(data => {
      const processed = processUsers(data);
      setUsers(processed);
    });
  }, []);
  
  return users;
};

const UserList = () => {
  const users = useUsers();
  return <ul>{users.map(u => <UserListItem key={u.id} user={u} />)}</ul>;
};
```

## Component Checklist

Before considering any component complete, verify:

**Atomic Classification**:
- [ ] Component fits clearly into one atomic category
- [ ] No atoms contain business logic
- [ ] No molecules fetch data or manage complex state
- [ ] Organisms are self-contained and independently functional
- [ ] Templates remain content-agnostic
- [ ] Pages handle all data fetching and business logic

**Modularity**:
- [ ] Single responsibility - component has one clear purpose
- [ ] Composed from smaller components, not monolithic
- [ ] No prop drilling beyond 2 levels
- [ ] All dependencies explicit through props or context
- [ ] Logic separated from presentation

**Code Quality**:
- [ ] Component file structure follows directory standards
- [ ] Props have TypeScript interfaces or PropTypes
- [ ] Unit tests cover component behavior
- [ ] Styles are scoped (CSS modules or styled-components)
- [ ] No magic numbers or hardcoded values
- [ ] Clear, descriptive component and prop names

**Storybook**:
- [ ] Stories file exists in component directory
- [ ] Meets minimum story count for atomic level
- [ ] All variants and states covered
- [ ] Interactive components have play function tests
- [ ] Responsive behavior tested
- [ ] ArgTypes defined for all props
- [ ] Complex organisms have MDX documentation
- [ ] Stories use mock data, no real API calls

**Reusability**:
- [ ] Component can be used in multiple contexts
- [ ] No hardcoded content or business-specific logic (except pages)
- [ ] Configurable through props
- [ ] Documented usage examples

## Anti-Patterns to Avoid

### God Components
Components that do everything. Break them down immediately.

### Anemic Atoms
Atoms that are too simple to be useful (wrapping `<div>` just to wrap it). Atoms should provide meaningful abstraction.

### Molecule Bloat
Molecules that grow too complex. Promote to organisms when they exceed 150 lines or combine more than 5 atoms.

### Template Specificity
Templates that assume specific content. Keep them abstract and reusable.

### Page Components
Creating reusable "page components." Pages are specific instances, not reusable components. Extract reusable parts into organisms or templates.

## Enforcement

This is not a suggestion. These are mandatory patterns. Code reviews must reject:
- Components misclassified in the atomic hierarchy
- Atoms with business logic
- Molecules fetching data
- Templates with specific content
- Poor separation of concerns
- Prop drilling beyond 2 levels
- Components mixing logic and presentation
- **Missing or incomplete Storybook stories**
- **Stories without interaction tests for interactive components**
- **Stories that violate atomic design principles**
- **Insufficient variant or state coverage in stories**

## Related Skills

The Frontend Developer implements UI components based on designs and API contracts.

### Upstream Skills (Provide Input)

| Skill | Provides | Developer Should Request |
|-------|----------|-------------------------|
| **TPO** | MRD with user flows | Interaction requirements, states |
| **Solutions Architect** | API contracts | Response formats, auth patterns |
| **UX Designer** | Designs, user flows | Figma files, interaction specs |

### Downstream/Parallel Skills

| Skill | Relationship | Coordination Point |
|-------|--------------|-------------------|
| **Frontend Tester** | Tests components/E2E | Test scenarios, accessibility |
| **Backend Developer** | Provides APIs | API contract alignment |
| **Tech Doc Writer** | Component documentation | Storybook, usage guides |
| **TPgM** | Tracks progress | Effort estimates, blockers |

### Consultation Triggers

**Consult UX Designer when:**
- Interaction patterns unclear
- Empty/error states need design
- Responsive behavior decisions
- Animation/motion design

**Consult Frontend Tester when:**
- Defining test scenarios
- Accessibility requirements
- E2E test coverage

**Consult Backend Developer when:**
- API contract questions
- Data format issues
- Real-time data needs

### Handoff Checklist

Before considering component complete:

```
□ UX Designer's designs implemented
□ Storybook stories complete
□ Frontend Tester has test strategy
□ Accessibility validated
□ TPgM updated on progress
```

### Skill Ecosystem Position

```
     ┌─────────────┐    ┌─────────────┐
     │     TPO     │    │ UX Designer │
     └──────┬──────┘    └──────┬──────┘
            │                  │
            └────────┬─────────┘
                     │
              ┌──────▼──────┐
              │  Solutions  │
              │  Architect  │
              └──────┬──────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
     Backend     Frontend     Data
     Developer   Developer   Platform
         │           │
         │           │
         ▼           ▼
     Backend     Frontend
     Tester      Tester
```

## Summary

Build maintainable, scalable, and testable frontend applications through disciplined architecture and comprehensive component documentation.

**Remember**: Consult UX Designer for design decisions and Frontend Tester for test strategy before implementation.
