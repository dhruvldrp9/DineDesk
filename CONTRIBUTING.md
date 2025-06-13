# Contributing to DineDesk

Thank you for your interest in contributing to DineDesk! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/dinedesk.git
   cd dinedesk
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements-production.txt
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys and configuration
   ```

4. **Database Setup**
   ```bash
   python setup_supabase_direct.py
   ```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and small

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with clear commit messages
3. Test your changes thoroughly
4. Update documentation if needed
5. Submit a pull request with description of changes

## Testing

Before submitting:
- Test both text chat and voice assistant interfaces
- Verify user authentication works correctly
- Check database operations function properly
- Test with different browsers for voice features

## Bug Reports

Include in bug reports:
- Operating system and browser version
- Steps to reproduce the issue
- Expected vs actual behavior
- Console error messages if any

## Feature Requests

For new features, please:
- Check existing issues first
- Describe the use case clearly
- Explain the expected behavior
- Consider implementation complexity