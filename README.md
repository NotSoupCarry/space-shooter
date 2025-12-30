# gh-space-shooter 🚀

A CLI tool that visualizes GitHub contribution graphs as gamified GIFs.

## Features

- 📊 Fetch GitHub contribution data (last 52 weeks)
- 📈 Display contribution statistics and recent activity
- 💾 Export data to JSON for further processing
- 🎮 (Coming soon) Generate gamified GIF animations

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd gh-space-shooter

# Install dependencies
uv sync

# Or using pip
pip install -e .
```

## Setup

1. Create a GitHub Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `read:user`
   - Copy the generated token

2. Set up your environment:
   ```bash
   # Copy the example env file
   cp .env.example .env

   # Edit .env and add your token
   # GH_TOKEN=your_token_here
   ```

   Alternatively, export the token directly:
   ```bash
   export GH_TOKEN=your_token_here
   # or
   export GH_TOKEN=your_token_here
   ```

## Usage

### Fetch contribution data

```bash
# Basic usage - display stats
gh-space-shooter fetch <username>

# Example
gh-space-shooter fetch torvalds

# Save data to JSON file
gh-space-shooter fetch torvalds --output torvalds_data.json

# Fetch without showing stats
gh-space-shooter fetch torvalds --no-stats
```

### Output

The tool displays:
- Total contributions over the last 52 weeks
- Number of active days
- Maximum daily contributions
- Average daily contributions
- Visual representation of the last 7 days

### Data Format

When saved to JSON, the data includes:
```json
{
  "username": "torvalds",
  "total_contributions": 1234,
  "weeks": [
    {
      "days": [
        {
          "date": "2024-01-01",
          "count": 5,
          "level": 2
        }
      ]
    }
  ],
  "fetched_at": "2024-12-30T12:00:00"
}
```

## Development

```bash
# Install in development mode
uv sync

# Run the CLI during development
uv run gh-space-shooter fetch <username>
```

## Roadmap

- [x] GitHub API integration
- [x] Contribution graph data fetching
- [x] CLI interface
- [ ] Game rules implementation
- [ ] GIF generation
- [ ] Gamified visualization

## License

MIT
