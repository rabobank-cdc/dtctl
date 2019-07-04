from dtctl.utils.state import ProgramState


class Api:
    pass


def test_program_state():
    api_object = Api()
    debug = False
    config = {
        'config_key_1': 1,
        'config_key_2': 'value'
    }
    config_file = '/test/config/file.json'

    program_state = ProgramState(api_object, debug, config, config_file)

    assert isinstance(program_state.api, Api)
    assert not program_state.debug
    assert program_state.config
    assert program_state.config['config_key_1'] == 1
    assert program_state.config_file == config_file
    assert isinstance(program_state.get_api(), Api)
    assert program_state.get_config_file() == config_file
