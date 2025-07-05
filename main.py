import asyncio
import aiofiles
import random

from form_workes.fillerForm import AsyncFillerForm
from form_workes.formConnetion import AsyncFormConnection
from settings import form_url, symbol_for_splitting_questions, random_s


def generate_random_string():
    num = random.randint(1, 5)
    return random_s[num]


async def process_form():
    async with AsyncFormConnection(form_url) as fc:
        filler = AsyncFillerForm(fc.get_driver())
        await filler.create()

        async with aiofiles.open('form_questions.txt', 'r', encoding='utf-8') as f:
            lines = await f.readlines()

        for line in lines:
            res = line.strip().split(symbol_for_splitting_questions)

            if res[0] == 'input':
                await filler.input_field(res[1], generate_random_string())
            elif res[0] == 'one':
                fc.switch_driver()
                await filler.one_of_the_list(res[1].strip())
            elif res[0] == 'few':
                fc.switch_driver()
                await filler.few_from_the_list(res[1].strip())

        print("Success")


async def main():
    coros = (process_form() for _ in range(3))
    await asyncio.gather(*coros)


if __name__ == '__main__':
    for i in range(100):
        asyncio.run(main())
