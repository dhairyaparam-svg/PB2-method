"""
Test script to verify PB2 web application setup
Run this before using the application to ensure all dependencies are installed
"""

import sys
import subprocess

def test_python_version():
    """Check Python version"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} - Requires 3.8+")
        return False
    print(f"✅ Python {version.major}.{version.minor} - OK")
    return True


def test_import(module_name, package_name=None):
    """Test if module can be imported"""
    print(f"Testing {module_name}...")
    try:
        __import__(module_name)
        print(f"✅ {module_name} - OK")
        return True
    except ImportError:
        package = package_name or module_name
        print(f"❌ {module_name} - Not installed")
        print(f"   Fix: pip install {package}")
        return False


def test_flask_app():
    """Test if Flask app can be imported"""
    print("Testing Flask application...")
    try:
        import flask
        from flask_cors import CORS
        print("✅ Flask setup - OK")
        return True
    except ImportError as e:
        print(f"❌ Flask setup - Failed: {e}")
        print("   Fix: pip install flask flask-cors")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("  PB2 Web Application - Setup Verification")
    print("=" * 60)
    print()

    results = []

    # Test Python version
    results.append(test_python_version())
    print()

    # Test core dependencies
    print("Testing core dependencies...")
    results.append(test_import("numpy"))
    results.append(test_import("scipy"))
    results.append(test_import("matplotlib"))
    results.append(test_import("sympy"))
    results.append(test_import("ezdxf"))
    print()

    # Test Flask
    results.append(test_flask_app())
    print()

    # Summary
    print("=" * 60)
    print("  Summary")
    print("=" * 60)

    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100

    print(f"Tests Passed: {passed}/{total} ({percentage:.0f}%)")
    print()

    if all(results):
        print("✅ All tests passed! Your setup is ready.")
        print()
        print("To start the web application:")
        print("  Windows: run_web.bat")
        print("  macOS/Linux: ./run_web.sh")
        print()
        print("Then open: http://localhost:5000")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print()
        print("To reinstall all dependencies:")
        print("  pip install --upgrade -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
