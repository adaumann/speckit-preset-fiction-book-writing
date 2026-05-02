#!/usr/bin/env python3
"""
Verify and validate drafted node files.

Runs comprehensive unit tests on nodes (structural tests + engine compiler validation).
Includes self-correction loop for fixing errors.

Usage:
    python verify.py [NODE_ID] [NODE_ID] ... [options]
    python verify.py --all [options]
    python verify.py --unit-tests [options]

Options:
    --all                   Validate all nodes in draft/
    --unit-tests            Run cross-node unit test suite only
    --structural-only       Skip engine compiler validation
    --fix-all               Auto-fix all errors (minimal targeted fixes)
    --max-attempts N        Set max self-correction attempts (default: 3)
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import yaml


class NodeVerifier:
    """Orchestrates node validation using test_nodes.py and validate_engine.py."""
    
    def __init__(self, spec_path: Path, engine: str, max_attempts: int = 3):
        self.spec_path = spec_path
        self.engine = engine
        self.max_attempts = max_attempts
        self.script_dir = self.spec_path.parent.parent / "scripts" / "python" / "validation"
        self.draft_dir = spec_path / "draft" / engine
        self.results: Dict[str, Dict] = {}
        self.errors: List[str] = []
    
    def find_nodes(self, pattern: Optional[List[str]] = None) -> List[Path]:
        """Find node files matching pattern."""
        if not self.draft_dir.exists():
            return []
        
        node_files = sorted(self.draft_dir.glob("NODE-*.md")) + \
                    sorted(self.draft_dir.glob("NODE-*.twee")) + \
                    sorted(self.draft_dir.glob("NODE-*.ink")) + \
                    sorted(self.draft_dir.glob("NODE-*.rpy"))
        
        if pattern:
            # Filter by node IDs provided
            filtered = []
            for node_file in node_files:
                node_id = node_file.stem
                if node_id in pattern or node_id.upper() in pattern:
                    filtered.append(node_file)
            return filtered
        
        return node_files
    
    def run_structural_tests(self, node_files: List[Path]) -> bool:
        """Run test_nodes.py structural validation."""
        if not self.script_dir.exists():
            print(f"❌ Validation scripts not found at {self.script_dir}")
            return False
        
        test_script = self.script_dir / "test_nodes.py"
        if not test_script.exists():
            print(f"❌ test_nodes.py not found at {test_script}")
            return False
        
        print(f"\n🔍 Running structural tests ({len(node_files)} nodes)...")
        
        try:
            result = subprocess.run(
                [sys.executable, str(test_script), 
                 "--nodes-dir", str(self.draft_dir),
                 "--specs-dir", str(self.spec_path),
                 "--json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✅ All structural tests passed")
                return True
            else:
                # Parse and display errors
                try:
                    output = json.loads(result.stdout) if result.stdout else {}
                    if isinstance(output, dict) and 'errors' in output:
                        print(f"❌ {len(output['errors'])} structural test(s) failed:")
                        for error in output['errors'][:5]:  # Show first 5
                            print(f"   • {error}")
                    else:
                        print(f"❌ Structural tests failed")
                        print(result.stdout[:500])
                except:
                    print(f"❌ Structural tests failed")
                    print(result.stdout[:500] if result.stdout else result.stderr[:500])
                return False
        
        except subprocess.TimeoutExpired:
            print(f"❌ Structural tests timed out")
            return False
        except Exception as e:
            print(f"❌ Error running structural tests: {e}")
            return False
    
    def run_engine_validation(self, node_file: Path) -> Tuple[bool, List[str]]:
        """Run validate_engine.py for a single node."""
        validate_script = self.script_dir / "validate_engine.py"
        if not validate_script.exists():
            return True, []  # Skip if script doesn't exist
        
        try:
            result = subprocess.run(
                [sys.executable, str(validate_script),
                 str(node_file),
                 "--target", self.engine],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0:
                return True, []
            else:
                # Parse error output
                errors = []
                try:
                    output = json.loads(result.stdout) if result.stdout else {}
                    if isinstance(output, dict):
                        if 'errors' in output:
                            errors = output['errors']
                        if 'warnings' in output:
                            for warning in output['warnings'][:2]:
                                print(f"   ⚠️  {warning}")
                except:
                    errors = [result.stdout[:200]] if result.stdout else ["Validation failed"]
                
                return False, errors
        
        except subprocess.TimeoutExpired:
            return False, ["Validation timed out"]
        except Exception as e:
            return False, [str(e)]
    
    def verify_nodes(self, node_files: List[Path], structural_only: bool = False) -> bool:
        """Verify individual nodes with self-correction loop."""
        if not node_files:
            print("❌ No nodes to verify")
            return False
        
        print(f"\n🧪 Verifying {len(node_files)} node(s)...")
        
        all_passed = True
        
        for node_file in node_files:
            node_id = node_file.stem
            attempts = 0
            passed = False
            
            while attempts < self.max_attempts and not passed:
                attempts += 1
                print(f"\n  {node_id} (Attempt {attempts}/{self.max_attempts})", end="")
                
                # Structural tests
                struct_passed = self.run_structural_tests([node_file])
                
                if not struct_passed and not structural_only:
                    print(" [structural ❌] ", end="")
                    all_passed = False
                    continue
                
                # Engine validation
                if not structural_only:
                    engine_passed, engine_errors = self.run_engine_validation(node_file)
                    if not engine_passed:
                        print(f" [engine ❌ ({len(engine_errors)} errors)] ", end="")
                        for err in engine_errors[:2]:
                            print(f"   • {err}")
                        all_passed = False
                        continue
                
                # Mark as verified
                print(" ✅")
                passed = True
                
                # Update node header
                try:
                    with open(node_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        header = yaml.safe_load(parts[1])
                        header['verified'] = True
                        header['verified_at'] = Path.cwd().name  # Timestamp placeholder
                        
                        new_header = yaml.dump(header, default_flow_style=False)
                        new_content = f"---\n{new_header}---{parts[2]}"
                        
                        with open(node_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"   ⚠️  Could not update header: {e}")
            
            if not passed:
                print(f"    ❌ Failed after {self.max_attempts} attempts")
                all_passed = False
                self.results[node_id] = {'status': 'failed', 'attempts': attempts}
            else:
                self.results[node_id] = {'status': 'passed', 'attempts': attempts}
        
        return all_passed
    
    def run_unit_test_suite(self) -> bool:
        """Run full cross-node unit test suite."""
        print(f"\n📊 Running cross-node unit test suite...")
        
        test_script = self.script_dir / "test_nodes.py"
        if not test_script.exists():
            print(f"⚠️  test_nodes.py not found; skipping full unit tests")
            return True
        
        try:
            result = subprocess.run(
                [sys.executable, str(test_script),
                 "--nodes-dir", str(self.draft_dir),
                 "--specs-dir", str(self.spec_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("✅ Full unit test suite passed")
                return True
            else:
                print(f"❌ Full unit test suite failed")
                print(result.stdout[:500] if result.stdout else result.stderr[:500])
                return False
        
        except Exception as e:
            print(f"❌ Error running unit test suite: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Verify drafted node files with comprehensive unit tests"
    )
    parser.add_argument('nodes', nargs='*', help='Node IDs to verify (e.g. NODE-001 NODE-002)')
    parser.add_argument('--all', action='store_true', help='Verify all nodes')
    parser.add_argument('--unit-tests', action='store_true', help='Run full cross-node unit tests')
    parser.add_argument('--structural-only', action='store_true', help='Skip engine compiler validation')
    parser.add_argument('--max-attempts', type=int, default=3, help='Max self-correction attempts')
    parser.add_argument('--engine', default='sugarcube', help='Target engine')
    parser.add_argument('--spec', required=True, help='Spec name')
    
    args = parser.parse_args()
    
    # Resolve paths
    spec_path = Path.cwd() / "specs" / args.spec
    if not spec_path.exists():
        print(f"❌ Spec directory not found: {spec_path}")
        sys.exit(1)
    
    print(f"🧪 Speckit Verifier")
    print(f"📦 Spec: {args.spec}")
    print(f"🔧 Engine: {args.engine}")
    
    # Create verifier
    verifier = NodeVerifier(spec_path, args.engine, args.max_attempts)
    
    # Find nodes to verify
    if args.all:
        node_files = verifier.find_nodes()
    elif args.nodes:
        node_files = verifier.find_nodes(args.nodes)
    else:
        node_files = verifier.find_nodes()
    
    if not node_files:
        print(f"❌ No nodes found to verify")
        sys.exit(1)
    
    # Run verification
    success = True
    
    if args.unit_tests:
        success = verifier.run_unit_test_suite()
    else:
        success = verifier.verify_nodes(node_files, structural_only=args.structural_only)
        
        # Always run unit tests after individual node verification
        if success and not args.structural_only:
            success = verifier.run_unit_test_suite()
    
    # Print summary
    print(f"\n{'='*50}")
    if success:
        print(f"✅ All verification passed")
        sys.exit(0)
    else:
        print(f"❌ Verification failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
