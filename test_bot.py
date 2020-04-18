import os
import asyncio
from tgintegration import BotController, InteractionClient


loop = asyncio.get_event_loop()

client = InteractionClient(
    session_name='test_bot',  # Arbitrary file path to the Pyrogram session file
    api_id=os.environ.get('BOT_API_ID'),  # See "Requirements" above, ...
    api_hash=os.environ.get('BOT_API_HASH'),  # alternatively use a `config.ini` file
)

client = BotController(
    bot_under_test='@Shop_final_task_bot',
    client=client,
    max_wait_response=15,  # Maximum timeout for bot re_sponses
    min_wait_consecutive=2  # Minimum time to wait for consecutive messages
)

async def test():
    await client.start()
    await client.clear_chat()

    response = await client.send_command_await('start', num_expected=1)

    assert response.num_messages == 1
    assert 'Dear customer!' in response.messages[0].text

    inline_keyboard = response.inline_keyboards[0]
    assert len(inline_keyboard.rows[0]) == 2

    response = await response.inline_keyboards[0].press_button_await(pattern='Add to cart')

    assert response.messages[0].text == 'Type in the name or ID of the product you want to add to your cart.'
    product = 'Skirt'
    response = await client.send_message_await(text=product)
    
    assert response.messages[0].text == f'How many {product} do you want?'
    quantity = '5'
    response = await client.send_message_await(text=quantity)

    assert response.messages[0].text == f'{product} in quantity of {quantity} added to your cart! Do you want to add anything else?'
    
    inline_keyboard = response.inline_keyboards[0]
    assert len(inline_keyboard.rows[0]) == 2

    response = await response.inline_keyboards[0].press_button_await(pattern='Yes')

    assert response.messages[0].text == 'Type in the name or ID of the product you want to add to your cart.'
    product = 'Pants'
    response = await client.send_message_await(text=product)

    assert 'Found following' in response.messages[0].text 
    product = 'Underpants'
    response = await client.send_message_await(text=product)

    assert 'Found following' in response.messages[0].text 
    id = '15'
    response = await client.send_message_await(text=id)
    
    product = 'String underpants'
    assert response.messages[0].text == f'How many {product} do you want?'
    quantity = '4'
    response = await client.send_message_await(text=quantity)

    assert response.messages[0].text == f'{product} in quantity of {quantity} added to your cart! Do you want to add anything else?'
    
    inline_keyboard = response.inline_keyboards[0]
    assert len(inline_keyboard.rows[0]) == 2

    response = await response.inline_keyboards[0].press_button_await(pattern='No')


if __name__ == '__,main__':
    loop.run_until_complete(test())
