# Component Test Patterns

React Testing Library patterns for comprehensive component testing.

## Setup

```typescript
// test-utils.tsx
import { render, RenderOptions } from '@testing-library/react'
import { ReactElement } from 'react'
import { ThemeProvider } from 'styled-components'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
  },
})

const AllProviders = ({ children }: { children: React.ReactNode }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        {children}
      </ThemeProvider>
    </QueryClientProvider>
  )
}

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: AllProviders, ...options })

export * from '@testing-library/react'
export { customRender as render }
```

---

## Query Patterns

### Priority Order (Use Top to Bottom)

```typescript
// 1. getByRole - accessible to everyone, most robust
screen.getByRole('button', { name: 'Submit' })
screen.getByRole('textbox', { name: 'Email' })
screen.getByRole('checkbox', { name: 'Accept terms' })
screen.getByRole('link', { name: 'Learn more' })
screen.getByRole('heading', { name: 'Dashboard', level: 1 })
screen.getByRole('list')
screen.getByRole('listitem')
screen.getByRole('dialog')
screen.getByRole('alert')
screen.getByRole('progressbar')

// 2. getByLabelText - form elements
screen.getByLabelText('Email address')
screen.getByLabelText(/password/i)

// 3. getByPlaceholderText - when no label
screen.getByPlaceholderText('Search...')

// 4. getByText - non-interactive elements
screen.getByText('Welcome back!')
screen.getByText(/error/i)

// 5. getByDisplayValue - input current value
screen.getByDisplayValue('current@email.com')

// 6. getByAltText - images
screen.getByAltText('User avatar')

// 7. getByTitle - elements with title attribute
screen.getByTitle('Close dialog')

// 8. getByTestId - last resort
screen.getByTestId('custom-dropdown')
```

### Query Variants

```typescript
// Single element (throws if not found or multiple)
getByRole('button')

// Single element (returns null if not found)
queryByRole('button')

// Multiple elements (throws if none found)
getAllByRole('listitem')

// Multiple elements (returns empty array if none)
queryAllByRole('listitem')

// Async - waits for element to appear
await findByRole('button')
await findAllByRole('listitem')
```

---

## Interaction Patterns

### User Events (Recommended)

```typescript
import userEvent from '@testing-library/user-event'

describe('interactions', () => {
  it('handles click', async () => {
    const user = userEvent.setup()
    const onClick = jest.fn()
    render(<Button onClick={onClick}>Click me</Button>)
    
    await user.click(screen.getByRole('button'))
    expect(onClick).toHaveBeenCalledTimes(1)
  })

  it('handles typing', async () => {
    const user = userEvent.setup()
    const onChange = jest.fn()
    render(<Input onChange={onChange} />)
    
    await user.type(screen.getByRole('textbox'), 'hello')
    expect(onChange).toHaveBeenCalledTimes(5) // once per character
    expect(screen.getByRole('textbox')).toHaveValue('hello')
  })

  it('handles clear and type', async () => {
    const user = userEvent.setup()
    render(<Input defaultValue="old" />)
    
    await user.clear(screen.getByRole('textbox'))
    await user.type(screen.getByRole('textbox'), 'new')
    expect(screen.getByRole('textbox')).toHaveValue('new')
  })

  it('handles keyboard', async () => {
    const user = userEvent.setup()
    render(<Input />)
    
    await user.type(screen.getByRole('textbox'), 'text{Enter}')
    // or
    await user.keyboard('{Enter}')
  })

  it('handles tab navigation', async () => {
    const user = userEvent.setup()
    render(
      <>
        <Input aria-label="First" />
        <Input aria-label="Second" />
      </>
    )
    
    await user.tab()
    expect(screen.getByLabelText('First')).toHaveFocus()
    
    await user.tab()
    expect(screen.getByLabelText('Second')).toHaveFocus()
  })

  it('handles select', async () => {
    const user = userEvent.setup()
    render(
      <select aria-label="Country">
        <option value="us">United States</option>
        <option value="uk">United Kingdom</option>
      </select>
    )
    
    await user.selectOptions(screen.getByRole('combobox'), 'uk')
    expect(screen.getByRole('combobox')).toHaveValue('uk')
  })

  it('handles checkbox', async () => {
    const user = userEvent.setup()
    render(<Checkbox label="Accept terms" />)
    
    const checkbox = screen.getByRole('checkbox')
    expect(checkbox).not.toBeChecked()
    
    await user.click(checkbox)
    expect(checkbox).toBeChecked()
  })

  it('handles file upload', async () => {
    const user = userEvent.setup()
    const onUpload = jest.fn()
    render(<FileInput onUpload={onUpload} />)
    
    const file = new File(['content'], 'test.png', { type: 'image/png' })
    const input = screen.getByLabelText('Upload file')
    
    await user.upload(input, file)
    expect(onUpload).toHaveBeenCalledWith(expect.objectContaining({
      name: 'test.png',
    }))
  })

  it('handles hover', async () => {
    const user = userEvent.setup()
    render(<Tooltip content="Help text">Hover me</Tooltip>)
    
    expect(screen.queryByText('Help text')).not.toBeInTheDocument()
    
    await user.hover(screen.getByText('Hover me'))
    expect(screen.getByText('Help text')).toBeInTheDocument()
    
    await user.unhover(screen.getByText('Hover me'))
    expect(screen.queryByText('Help text')).not.toBeInTheDocument()
  })
})
```

---

## Async Patterns

### Waiting for Elements

```typescript
// findBy - waits for element to appear
it('shows data after loading', async () => {
  render(<UserProfile id="123" />)
  
  // Initially shows loading
  expect(screen.getByRole('progressbar')).toBeInTheDocument()
  
  // Wait for content
  const userName = await screen.findByText('John Doe')
  expect(userName).toBeInTheDocument()
  
  // Loading should be gone
  expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
})

// waitFor - waits for assertion to pass
it('enables button after validation', async () => {
  const user = userEvent.setup()
  render(<Form />)
  
  const submitButton = screen.getByRole('button', { name: 'Submit' })
  expect(submitButton).toBeDisabled()
  
  await user.type(screen.getByLabelText('Email'), 'valid@email.com')
  
  await waitFor(() => {
    expect(submitButton).toBeEnabled()
  })
})

// waitForElementToBeRemoved
it('hides modal on close', async () => {
  const user = userEvent.setup()
  render(<Modal open={true} />)
  
  await user.click(screen.getByRole('button', { name: 'Close' }))
  
  await waitForElementToBeRemoved(() => screen.queryByRole('dialog'))
})
```

### Async Gotchas

```typescript
// WRONG - assertion might run before state updates
it('broken async test', () => {
  render(<AsyncComponent />)
  fireEvent.click(screen.getByRole('button'))
  expect(screen.getByText('Done')).toBeInTheDocument() // Might fail
})

// CORRECT - wait for the result
it('working async test', async () => {
  render(<AsyncComponent />)
  fireEvent.click(screen.getByRole('button'))
  expect(await screen.findByText('Done')).toBeInTheDocument()
})

// CORRECT - use userEvent (returns promise)
it('also working', async () => {
  const user = userEvent.setup()
  render(<AsyncComponent />)
  await user.click(screen.getByRole('button'))
  expect(await screen.findByText('Done')).toBeInTheDocument()
})
```

---

## State Testing Patterns

### Loading State

```typescript
it('shows loading indicator', () => {
  render(<DataList isLoading={true} />)
  
  expect(screen.getByRole('progressbar')).toBeInTheDocument()
  expect(screen.queryByRole('list')).not.toBeInTheDocument()
})

it('shows skeleton during load', () => {
  render(<Card isLoading={true} />)
  
  expect(screen.getByTestId('skeleton')).toBeInTheDocument()
  expect(screen.queryByRole('heading')).not.toBeInTheDocument()
})
```

### Error State

```typescript
it('displays error message', () => {
  render(<DataList error="Failed to load" />)
  
  expect(screen.getByRole('alert')).toHaveTextContent('Failed to load')
  expect(screen.getByRole('button', { name: 'Retry' })).toBeInTheDocument()
})

it('shows inline field error', async () => {
  const user = userEvent.setup()
  render(<Form />)
  
  await user.type(screen.getByLabelText('Email'), 'invalid')
  await user.tab() // trigger blur validation
  
  expect(screen.getByRole('textbox', { name: 'Email' })).toHaveAccessibleDescription('Invalid email format')
})
```

### Empty State

```typescript
it('shows empty state when no data', () => {
  render(<DataList items={[]} />)
  
  expect(screen.getByText('No items yet')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Add item' })).toBeInTheDocument()
})
```

### Disabled State

```typescript
it('disables form during submission', async () => {
  const user = userEvent.setup()
  render(<Form />)
  
  await user.click(screen.getByRole('button', { name: 'Submit' }))
  
  expect(screen.getByRole('button', { name: 'Submit' })).toBeDisabled()
  expect(screen.getByLabelText('Email')).toBeDisabled()
})
```

---

## Form Testing Patterns

### Form Submission

```typescript
it('submits form with valid data', async () => {
  const user = userEvent.setup()
  const onSubmit = jest.fn()
  render(<ContactForm onSubmit={onSubmit} />)
  
  await user.type(screen.getByLabelText('Name'), 'John Doe')
  await user.type(screen.getByLabelText('Email'), 'john@example.com')
  await user.type(screen.getByLabelText('Message'), 'Hello!')
  
  await user.click(screen.getByRole('button', { name: 'Send' }))
  
  expect(onSubmit).toHaveBeenCalledWith({
    name: 'John Doe',
    email: 'john@example.com',
    message: 'Hello!',
  })
})
```

### Form Validation

```typescript
describe('form validation', () => {
  it('shows required field errors', async () => {
    const user = userEvent.setup()
    render(<Form />)
    
    await user.click(screen.getByRole('button', { name: 'Submit' }))
    
    expect(screen.getByText('Name is required')).toBeInTheDocument()
    expect(screen.getByText('Email is required')).toBeInTheDocument()
  })

  it('validates email format', async () => {
    const user = userEvent.setup()
    render(<Form />)
    
    await user.type(screen.getByLabelText('Email'), 'not-an-email')
    await user.tab()
    
    expect(screen.getByText('Invalid email format')).toBeInTheDocument()
  })

  it('validates on blur', async () => {
    const user = userEvent.setup()
    render(<Form />)
    
    const emailInput = screen.getByLabelText('Email')
    await user.click(emailInput)
    await user.tab()
    
    expect(screen.getByText('Email is required')).toBeInTheDocument()
  })
})
```

---

## Modal/Dialog Testing

```typescript
describe('Modal', () => {
  it('opens when trigger clicked', async () => {
    const user = userEvent.setup()
    render(<ModalWithTrigger />)
    
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    
    await user.click(screen.getByRole('button', { name: 'Open' }))
    
    expect(screen.getByRole('dialog')).toBeInTheDocument()
    expect(screen.getByRole('dialog')).toHaveAttribute('aria-modal', 'true')
  })

  it('closes on escape key', async () => {
    const user = userEvent.setup()
    render(<Modal open={true} onClose={jest.fn()} />)
    
    await user.keyboard('{Escape}')
    
    await waitForElementToBeRemoved(() => screen.queryByRole('dialog'))
  })

  it('traps focus within modal', async () => {
    const user = userEvent.setup()
    render(<Modal open={true} />)
    
    const closeButton = screen.getByRole('button', { name: 'Close' })
    const confirmButton = screen.getByRole('button', { name: 'Confirm' })
    
    // Focus should be trapped within modal
    closeButton.focus()
    await user.tab()
    expect(confirmButton).toHaveFocus()
    
    await user.tab()
    expect(closeButton).toHaveFocus() // Wraps back
  })
})
```

---

## List/Table Testing

```typescript
describe('DataTable', () => {
  const items = [
    { id: 1, name: 'Item 1', status: 'active' },
    { id: 2, name: 'Item 2', status: 'inactive' },
  ]

  it('renders all items', () => {
    render(<DataTable items={items} />)
    
    expect(screen.getAllByRole('row')).toHaveLength(3) // header + 2 items
    expect(screen.getByText('Item 1')).toBeInTheDocument()
    expect(screen.getByText('Item 2')).toBeInTheDocument()
  })

  it('sorts by column', async () => {
    const user = userEvent.setup()
    render(<DataTable items={items} />)
    
    await user.click(screen.getByRole('columnheader', { name: 'Name' }))
    
    const rows = screen.getAllByRole('row')
    expect(rows[1]).toHaveTextContent('Item 1')
    expect(rows[2]).toHaveTextContent('Item 2')
  })

  it('filters items', async () => {
    const user = userEvent.setup()
    render(<DataTable items={items} />)
    
    await user.type(screen.getByRole('searchbox'), 'Item 1')
    
    expect(screen.getAllByRole('row')).toHaveLength(2) // header + 1 match
    expect(screen.getByText('Item 1')).toBeInTheDocument()
    expect(screen.queryByText('Item 2')).not.toBeInTheDocument()
  })

  it('selects item', async () => {
    const user = userEvent.setup()
    const onSelect = jest.fn()
    render(<DataTable items={items} onSelect={onSelect} />)
    
    await user.click(screen.getByRole('checkbox', { name: 'Select Item 1' }))
    
    expect(onSelect).toHaveBeenCalledWith([1])
  })
})
```

---

## Snapshot Testing (Use Sparingly)

```typescript
// Only for stable, visual components
it('matches snapshot', () => {
  const { container } = render(<Icon name="check" />)
  expect(container).toMatchSnapshot()
})

// Better: inline snapshots for small outputs
it('renders correct structure', () => {
  const { container } = render(<Badge>New</Badge>)
  expect(container.innerHTML).toMatchInlineSnapshot(
    `"<span class="badge badge-default">New</span>"`
  )
})
```

---

## Anti-Patterns to Avoid

```typescript
// ❌ Testing implementation details
expect(component.state.isOpen).toBe(true)
expect(wrapper.find('.internal-class')).toHaveLength(1)

// ✅ Test behavior/output
expect(screen.getByRole('dialog')).toBeVisible()

// ❌ Using test IDs when accessible queries work
screen.getByTestId('submit-button')

// ✅ Use accessible queries
screen.getByRole('button', { name: 'Submit' })

// ❌ Hardcoded waits
await new Promise(r => setTimeout(r, 1000))

// ✅ Wait for specific condition
await waitFor(() => expect(button).toBeEnabled())

// ❌ Multiple assertions without context
expect(x).toBe(1)
expect(y).toBe(2)
expect(z).toBe(3)

// ✅ Group related assertions or test separately
expect(result).toEqual({ x: 1, y: 2, z: 3 })
```
