import argparse
import subprocess


ENVIRONMENTS = {
    "staging": "devops-staging",
    "production": "devops-production",
}


def build_commands(environment, image):
    namespace = ENVIRONMENTS[environment]
    return [
        ["kubectl", "-n", namespace, "set", "image", "deployment/app", f"app={image}"],
        ["kubectl", "-n", namespace, "rollout", "status", "deployment/app", "--timeout=120s"],
        ["kubectl", "-n", namespace, "run", "smoke-test", "--rm", "--restart=Never", "--image=curlimages/curl:8.8.0", "--", "curl", "-fsS", "http://app/health"],
    ]


def deploy(environment, image, execute=False):
    commands = build_commands(environment, image)
    for command in commands:
        print("$", " ".join(command))
        if execute:
            subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(description="Deploy an immutable image to Kubernetes.")
    parser.add_argument("--environment", choices=sorted(ENVIRONMENTS), required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--execute", action="store_true", help="Run kubectl commands instead of printing them")
    args = parser.parse_args()
    deploy(args.environment, args.image, args.execute)


if __name__ == "__main__":
    main()
