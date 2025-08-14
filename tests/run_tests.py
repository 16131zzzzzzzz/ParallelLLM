#!/usr/bin/env python3
"""
测试运行脚本
提供不同级别的测试选项
"""
import argparse
import os
import sys
import subprocess
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def run_unit_tests():
    """运行单元测试（Mock测试）"""
    print("🧪 Running Unit Tests (Mock API calls)...")
    
    test_files = [
        "tests/test_client.py",
        "tests/test_openai_provider.py", 
        "tests/test_siliconflow_provider.py",
        "tests/test_anthropic_provider.py",
        "tests/test_google_provider.py",
        "tests/test_deepseek_provider.py",
        "tests/test_zhipu_provider.py",
        "tests/test_load_balancing.py"
    ]
    
    success = True
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📝 Running {test_file}...")
            result = subprocess.run([sys.executable, "-m", "unittest", test_file], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ {test_file} FAILED")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                success = False
            else:
                print(f"✅ {test_file} PASSED")
        else:
            print(f"⚠️  {test_file} not found, skipping...")
    
    return success


def run_integration_tests():
    """运行集成测试（需要真实API密钥）"""
    print("🔗 Running Integration Tests (Real API calls)...")
    
    if not os.getenv("SILICONFLOW_API_KEY"):
        print("⚠️  No SILICONFLOW_API_KEY found. Integration tests will be skipped.")
        return True
    
    test_files = [
        "tests/manual_test.py",
        "tests/multi_key_test.py"
    ]
    
    success = True
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📝 Running {test_file}...")
            result = subprocess.run([sys.executable, "-m", "unittest", test_file],
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ {test_file} FAILED")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                success = False
            else:
                print(f"✅ {test_file} PASSED")
        else:
            print(f"⚠️  {test_file} not found, skipping...")
    
    return success


def run_provider_specific_tests(provider_name):
    """运行特定提供商的测试"""
    print(f"🏢 Running tests for {provider_name} provider...")
    
    test_file = f"tests/test_{provider_name}_provider.py"
    
    if not os.path.exists(test_file):
        print(f"❌ Test file {test_file} not found!")
        return False
    
    result = subprocess.run([sys.executable, "-m", "unittest", test_file],
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ {provider_name} provider tests FAILED")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False
    else:
        print(f"✅ {provider_name} provider tests PASSED")
        return True


def run_all_tests():
    """运行所有测试"""
    print("🚀 Running ALL tests...")
    
    unit_success = run_unit_tests()
    integration_success = run_integration_tests()
    
    if unit_success and integration_success:
        print("\n🎉 ALL TESTS PASSED!")
        return True
    else:
        print("\n💥 SOME TESTS FAILED!")
        return False


def main():
    parser = argparse.ArgumentParser(description="PLLM Test Runner")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--provider", type=str, help="Run tests for specific provider")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    success = True
    
    if args.unit:
        success = run_unit_tests()
    elif args.integration:
        success = run_integration_tests()
    elif args.provider:
        success = run_provider_specific_tests(args.provider)
    elif args.all:
        success = run_all_tests()
    else:
        # 默认运行单元测试
        print("No specific test type specified, running unit tests by default...")
        print("Use --help to see all options")
        success = run_unit_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()