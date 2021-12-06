import argparse
import os
import pathlib
from time import sleep

import requests


def parser():
    parser = argparse.ArgumentParser(description='Transform command')

    parser.add_argument('-f', '--file', type=str, help='file to transform')
    parser.add_argument('-o', '--output_directory', type=str, help='Output directory')
    parser.add_argument('-tp', '--type', type=str, help='comma separated transform types')
    parser.add_argument('-t', '--token', type=str, help='API token')
    parser.add_argument('-e', '--enhance', action='store_true', help='Use enhancement')
    parser.add_argument('-d', '--denoise', action='store_true', help='Use denoise')
    parser.add_argument('-u', '--upscale', type=int, help='Upscale paramater - 2,3 or 4.')

    return parser


def transform_file(args):
    files = {'image': open(args.file, 'rb')}
    types = []

    if args.type:
        types = args.type.split(',')
    else:
        if args.upscale:
            types.append(f'ganzoom{args.upscale}-jpg90')
        if args.enhance:
            types.append('ganenhance1-jpg90')
        if args.denoise:
            types.append('ganzoomnoise1-jpg90')

    url = 'https://deep-image.ai/rest_api/deep_image/transform'

    headers = {
        'x-api-key': args.token,
        'x-application-name': 'deep_image'
    }

    print(f'Sending file to transform with options: {types}')
    values = {'transformations': types}

    r = requests.post(url, files=files, data=values, headers=headers)
    r = r.json()
    print('Getting job...')
    job = r.get('job')

    url = f'https://deep-image.ai/rest_api/deep_image/result/{job}'

    data = {}
    for i in range(100):
        print('Waiting for job results...')
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(f'Something went wrong {r.text}')
            exit()
        data = r.json()
        if data.get('status') == 'complete':
            break
        sleep(1)

    result_url = data.get('result_url')
    if result_url:
        r = requests.get(result_url)
        path = pathlib.Path(args.file)
        output_dir = args.output_directory if args.output_directory else pathlib.Path(args.file).parent
        new_name = f'{path.stem}-output{path.suffix}'
        output_file = os.path.join(output_dir, new_name)

        with open(output_file, 'wb') as f:
            f.write(r.content)
        print(f'Saving result at {output_file}')
    else:
        print(f'Something went wrong - {data}')


if __name__ == '__main__':
    args = parser().parse_args()
    transform_file(args)
