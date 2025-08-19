# Video Transcription Pro

## Contributing Guidelines

We welcome contributions to Video Transcription Pro! This document provides guidelines for contributing to the project.

## 🤝 Ways to Contribute

- **Bug Reports**: Report bugs via GitHub Issues
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests with bug fixes or new features
- **Documentation**: Improve documentation, examples, or tutorials
- **Testing**: Add test cases or improve test coverage

## 🚀 Getting Started

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/video-transcription-pro.git
   cd video-transcription-pro
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .[dev]
   ```

3. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests and quality checks**
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Check code formatting
   black src/ tests/ examples/
   
   # Check code style
   flake8 src/ tests/ examples/
   
   # Type checking
   mypy src/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Code Style

### Python Code Standards

- Follow **PEP 8** style guidelines
- Use **Black** for code formatting (configured in `pyproject.toml`)
- Use **type hints** for function parameters and return values
- Write **docstrings** for all public functions and classes
- Maximum line length: **88 characters** (Black default)

### Docstring Format

Use Google-style docstrings:

```python
def process_video(video_path: str, output_dir: str) -> Dict:
    """
    Process a video file for transcription.
    
    Args:
        video_path: Path to the input video file
        output_dir: Directory for output files
        
    Returns:
        Dictionary containing processing results
        
    Raises:
        FileNotFoundError: If video file doesn't exist
        
    Example:
        >>> result = process_video("video.mp4", "output/")
        >>> print(f"Success: {result['success']}")
    """
```

### Commit Message Format

Use conventional commit format:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for adding or updating tests
- `refactor:` for code refactoring
- `perf:` for performance improvements
- `ci:` for CI/CD changes

Examples:
```
feat: add GPU acceleration for speaker diarization
fix: resolve memory leak in batch processing
docs: update API documentation for VideoTranscriber
test: add integration tests for pipeline
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=video_transcription --cov-report=html

# Run specific test file
pytest tests/test_video_transcription.py -v

# Run tests matching pattern
pytest -k "test_transcriber" -v
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Include both unit tests and integration tests
- Mock external dependencies (file I/O, network calls)
- Test edge cases and error conditions

Example test structure:
```python
class TestVideoTranscriber:
    """Test cases for VideoTranscriber class."""
    
    def test_init_default(self):
        """Test default initialization."""
        transcriber = VideoTranscriber()
        assert transcriber.model_name == "large-v3"
    
    def test_invalid_model_raises_error(self):
        """Test that invalid model raises ValueError."""
        with pytest.raises(ValueError):
            VideoTranscriber(model="invalid")
```

## 📚 Documentation

### Documentation Standards

- Keep README.md updated with new features
- Add docstrings to all public APIs
- Include code examples in documentation
- Update API documentation when making changes
- Write clear, concise explanations

### Building Documentation

```bash
cd docs/
make html
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Python version** and operating system
2. **Package version** of video-transcription-pro
3. **Complete error message** and stack trace
4. **Minimal code example** that reproduces the issue
5. **Expected vs actual behavior**
6. **Hardware information** (GPU model if using GPU acceleration)

Use this template:

```markdown
## Bug Description
Brief description of the issue

## Environment
- Python version: 3.9.7
- Package version: 1.0.0
- OS: Windows 11 / Ubuntu 20.04 / macOS 12
- GPU: NVIDIA RTX 3070 (if applicable)

## Reproduction Steps
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Error Message
```
Full error traceback here
```

## Code Example
```python
# Minimal code that reproduces the issue
```

## 💡 Feature Requests

For feature requests, please include:

1. **Clear description** of the proposed feature
2. **Use case** explaining why it's needed
3. **Proposed API** or interface design
4. **Implementation suggestions** (if you have ideas)

## 🔍 Code Review Process

All contributions go through code review:

1. **Automated checks** must pass (tests, linting, formatting)
2. **Manual review** by maintainers
3. **Discussion** and feedback incorporation
4. **Approval** and merge

### Review Criteria

- Code quality and style
- Test coverage
- Documentation completeness
- Performance implications
- Backward compatibility
- Security considerations

## 📋 Issue Labels

We use these labels to organize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to docs
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `priority: high`: High priority issues
- `needs: tests`: Needs test coverage
- `needs: docs`: Needs documentation

## 🎉 Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md** file
- **Release notes** for significant contributions
- **GitHub contributors** section

## 📞 Getting Help

If you need help with contributing:

- **GitHub Discussions** for general questions
- **GitHub Issues** for specific problems
- **Email** maintainers for private matters

## 📜 Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

---

Thank you for contributing to Video Transcription Pro! 🎉
