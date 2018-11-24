import argparse
import textwrap
import yaml
import os


def main():
    parser = argparse.ArgumentParser(
        description="utility to update README.md etc. from exceptions.yml"
    )
    parser.add_argument(
        '--root', default='',
        help='path to root of project directory, defaulting to the current directory'
    )
    args = parser.parse_args()

    exception_data = load_exception_data(args.root)

    update_readme(args.root, exception_data)


def load_exception_data(repo_root):
    exception_data_path = os.path.join(repo_root, "exceptions.yml")
    with open(exception_data_path) as exception_file:
        return yaml.load(exception_file)


def update_readme(repo_root, exception_data):
    resources_directory = os.path.join(repo_root, "resources")
    readme_template_path = os.path.join(resources_directory, "README.template.md")
    with open(readme_template_path) as readme_template_file:
        readme_template = readme_template_file.read()

    output_readme_path = os.path.join(repo_root, "README.md")
    with open(output_readme_path, 'w') as output_readme_file:
        def md(text, end='\n'):
            output_readme_file.write(f"{text}{end}")

        def blankline():
            md("")

        def blanklines(count):
            [blankline() for _ in range(count)]

        def bullet_point(text):
            md(f"* {text}")

        def heading(title, level, blankline_afterwards=True):
            md(f"{'#' * level} {title}")
            if blankline_afterwards:
                blankline()

        output_readme_file.write(readme_template)
        blanklines(2)

        heading("Exceptions", level=1, blankline_afterwards=False)

        md(textwrap.dedent("""
            Below are assorted programs and the domains they are believed to access. Adding these domains to your
            proxy exceptions should allow these programs to operate normally.
        """))

        for program in sorted(exception_data):
            information = exception_data[program]
            domains = information["domains"]
            tags = information["tags"]

            heading(program, level=2)

            md(f"Tags: {', '.join(map(format_tag, tags))}")
            blankline()

            heading("Domains", level=3)

            for domain in domains:
                bullet_point(f"[{domain}]({domain})")

            blankline()


def format_tag(tag_text):
    if '=' in tag_text:
        key, value = tag_text.split("=", maxsplit=1)
        return f"_{key}_=**{value}**"
    else:
        return f"_{tag_text}_"


if __name__ == "__main__":
    main()
