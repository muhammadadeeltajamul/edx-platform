import sys
import os
import yaml
import argparse
import json


def get_all_unit_test_shards():
    unit_tests_json = f'{os.getcwd()}/.github/workflows/unit-test-shards.json'
    with open(unit_tests_json) as file:
        unit_test_workflow_shards = json.loads(file.read())

    return unit_test_workflow_shards


def get_modules_except_cms():
    all_unit_test_shards = get_all_unit_test_shards()
    return set([shard.get('path') for shard in all_unit_test_shards.items() if not shard.get('settings').startswith('cms')])

def get_cms_modules():
    all_unit_test_shards = get_all_unit_test_shards()
    return set([shard.get('path') for shard in all_unit_test_shards.items() if shard.get('settings').startswith('cms')])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cms-only", action="store_true", default="")
    parser.add_argument("--lms-only", action="store_true", default="")
    argument = parser.parse_args()

    if not argument.cms_only and not argument.lms_only:
        print("Please specify --cms-only or --lms-only")
        sys.exit(1)

    modules = get_cms_modules() if argument.cms_only else get_modules_except_cms()
    paths_output = ' '.join(modules)
    sys.stdout.write(paths_output)
