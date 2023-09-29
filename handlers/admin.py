import os

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from loader import bot, base
from keyboard.inline import admin_manager_kb, admin_cancel_kb
from utils.helpers import show_priority_drivers_text
from states.admin import AdminComands


async def admin_manager(message: types.Message):
    """ Управление админкой """
    admins = os.getenv('ADMIN').split(',')
    if str(message.from_user.id) in admins:
        await bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=admin_manager_kb())


async def show_staff(callback: types.CallbackQuery):
    """ Показать всех приоритетных водителей """
    await callback.answer()
    data = base.get_staff_driver()
    if data:
        text = show_priority_drivers_text(data)
        await callback.message.edit_text(text=text, reply_markup=admin_cancel_kb())
    else:
        await callback.message.edit_text('🙅 Ни одного водителя не добавлено', reply_markup=admin_cancel_kb())


async def get_phone_staff(callback: types.CallbackQuery, state: FSMContext):
    """ Ввести номер водителя """
    await callback.answer()
    callback_data = callback.data.split('__')[0]
    if callback_data == 'add':
        await callback.message.edit_text('Введите номер для добавления с префиксом "add"\nПример: add +79377788899',
                                         reply_markup=admin_cancel_kb())
        await state.set_state(AdminComands.get_phone)
    else:
        await callback.message.edit_text('Введите номер для удаления с префиксом "del"\nПример: del +79377788899',
                                         reply_markup=admin_cancel_kb())
        await state.set_state(AdminComands.get_phone)


async def new_staff(message: types.Message, state: FSMContext):
    """ Добавление/удаление приоритета водителям """

    text = message.text.split(' ')
    if len(text) < 2:
        await bot.send_message(
            message.from_user.id,
            'Не корректный формат, попробуйте еще раз',
            reply_markup=admin_cancel_kb()
        )
        return
    action, phone = text[0], text[-1]
    user = base.get_user(phone=phone)
    if user:
        if action == 'add':
            if user.get('is_staff'):
                await bot.send_message(message.from_user.id,
                                       f'У водителя {user.get("full_name")} с номером {phone} уже есть приоритет',
                                       reply_markup=admin_cancel_kb())
            else:
                update = base.update_driver_status(phone=phone, status=True)
                if update:
                    await bot.send_message(
                        message.from_user.id,
                        f'Водителю {user.get("full_name")} с номером {user.get("phone")} назначен приоритет',
                        reply_markup=admin_cancel_kb()
                    )
                else:
                    await bot.send_message(message.from_user.id,
                                           f'Ошибка при попытке добавления приоритета водителю {user.get("full_name")}',
                                           reply_markup=admin_cancel_kb())
        else:
            update = base.update_driver_status(phone=phone, status=False)
            if update:
                await bot.send_message(
                    message.from_user.id,
                    f'У водителя {user.get("full_name")} с номером {user.get("phone")} больше нет приоритета',
                    reply_markup=admin_cancel_kb()
                )
            else:
                await bot.send_message(message.from_user.id,
                                       f'Ошибка при попытке изменения приоритета водителю {user.get("full_name")}',
                                       reply_markup=admin_cancel_kb())
    else:
        await bot.send_message(message.from_user.id,
                               f'Пользователь с номером {phone} не зарегистрирован в боте',
                               reply_markup=admin_cancel_kb()
                               )
    await state.clear()


async def admin_stat(callback: types.CallbackQuery):
    """ Статистика по водителям """
    await callback.answer()
    driver_count = base.get_drivers_count()
    await callback.message.edit_text(f'В боте зарегистрировано: {driver_count}', reply_markup=admin_cancel_kb())


async def admin_cancel(callback: types.CallbackQuery, state: FSMContext):
    """ Вернуться в главое меню админки """
    await callback.answer()
    await state.clear()
    await callback.message.edit_text('Выберите действие:', reply_markup=admin_manager_kb())


def admin_handlers(dp: Dispatcher):
    dp.message.register(admin_manager, F.text == '/admin')
    dp.callback_query.register(show_staff, F.data == 'show_staff')
    dp.callback_query.register(get_phone_staff, F.data.endswith('__staff'))
    dp.callback_query.register(admin_stat, F.data == 'admin_stat')
    dp.callback_query.register(admin_cancel, F.data == 'cancel_admin')
    dp.message.register(new_staff, AdminComands.get_phone)
