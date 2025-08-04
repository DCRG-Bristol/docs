import subprocess
import sys

def run(cmd, cwd=None):
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(cmd, cwd=cwd, text=True, shell=False,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def get_submodules():
    """Return a list of submodule paths from .gitmodules."""
    success, output = run(["git", "config", "--file", ".gitmodules", "--get-regexp", "path"])
    if not success:
        print("Error reading .gitmodules")
        sys.exit(1)
    return [line.split()[1] for line in output.splitlines()]

def update_submodule(path, branch):
    print(f"\nUpdating submodule: {path}")
    steps = [
        (["git", "fetch", "origin", branch], "Fetching"),
        (["git", "checkout", branch], "Checking out branch"),
        (["git", "merge", f"origin/{branch}"], "Merging origin branch"),
    ]
    for cmd, desc in steps:
        success, output = run(cmd, cwd=path)
        print(f"{desc}... {'OK' if success else 'FAILED'}")
        if not success:
            print(output)
            return False
    return True

def main():
    branch = sys.argv[1] if len(sys.argv) > 1 else "master"
    print(f"Updating all submodules to latest on branch '{branch}'")

    submodules = get_submodules()
    for path in submodules:
        success = update_submodule(path, branch)
        if success:
            run(["git", "add", path])

    print("\nDone.")
    print("Now commit and push the changes in the parent repo:")
    print(f"  git commit -m \"Update submodules to latest on '{branch}'\"")
    print("  git push")

if __name__ == "__main__":
    main()
