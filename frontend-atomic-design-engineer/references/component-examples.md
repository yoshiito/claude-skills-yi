# Component Examples by Atomic Level

Detailed code examples for each level of the atomic design hierarchy.

## Atoms

### Correct Atom Example

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
```

### Incorrect Atom Example

```javascript
// ✗ WRONG: Business logic in atom
const Button = ({ userId, onClick }) => {
  const user = fetchUser(userId); // NO - atoms don't fetch data
  return <button onClick={onClick}>{user.name}</button>;
};
```

## Molecules

### Correct Molecule Example

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
```

### Incorrect Molecule Example

```javascript
// ✗ WRONG: Too complex for molecule
const SearchField = ({ endpoint, filters, onResults }) => {
  const results = await fetchSearchResults(endpoint, filters); // NO
  return <div>...</div>;
};
```

## Organisms

### Correct Organism Example

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
```

### Incorrect Organism Example

```javascript
// ✗ WRONG: Too much business logic
const ProductCard = ({ productId }) => {
  const product = useProductDetails(productId);
  const cart = useCart();
  const favorites = useFavorites();
  const recommendations = useRecommendations(productId);
  // NO - this is template territory, too much data orchestration
};
```

## Templates

### Correct Template Example

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
```

### Incorrect Template Example

```javascript
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

## Pages

### Correct Page Example

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

## Modularity Patterns

### Single Responsibility

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

### Composition Over Inheritance

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

### Prop Drilling vs Context

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

### Explicit Dependencies

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

### Separation of Logic and Presentation

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
