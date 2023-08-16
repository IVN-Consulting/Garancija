def setup():
    pass

<<<<<<< Updated upstream
#comment
=======
def increment(i):
    print("izvrsio sam se")
    return i

def f():
    result = increment(123)
    return result


def atest_f_with_spy(mocker):
    increment_spy = mocker.spy(tests, 'increment')

    f()

    increment_spy.assert_called_once()


def atest_f_calls_increment(mocker):
    # Given
    increment_mock = mocker.patch('tests.increment')

    # When
    f()

    # Then
    increment_mock.assert_called_once()


def atest_f_values(mocker):
    # Given
    increment_mock = mocker.patch('tests.increment')
    increment_mock.return_value = 123

    # When
    actual_result = f()

    # Then
    assert actual_result == 123


def atest_prvi(mocker):
    # Given
    group_workspaces = {
        'User Service': ['Authentication', 'User Management'],
        'Shop Service': ['Shop API'],
        'Warranty Service': ['Warranty API']
    }
    frontend = FrontendAPI(_type="myhome")
    backend = BackendAPI(_type="group", workspaces=group_workspaces, _filter=True)
    syncer = Syncer(backend=backend, frontend_api=frontend)

    get_workspaces_spy = mocker.spy(BackendAPI, 'get_workspaces')
    frontend_sync_mock = mocker.patch.object(FrontendAPI, 'sync')

    # When
    syncer.sync()

    # Then
    get_workspaces_spy.assert_called_once_with(backend, enrich_with_apigroups=True)
    assert frontend_sync_mock.call_count == 4
    expected_xano_instance = "GROUP"
    expected_xano_host = "https://ivn-consulting.com/group"


    call1 = mocker.call(
        xano_instance=expected_xano_instance,
        xano_workspace="User Service",
        backendgroup="Authentication",
        xano_canonical="authentication",
        xano_host=expected_xano_host,
    )
    call2 = mocker.call(
        xano_instance=expected_xano_instance,
        xano_workspace="User Service",
        backendgroup="User Management",
        xano_canonical="user-management",
        xano_host=expected_xano_host,
    )
    call3 = mocker.call(
        xano_instance=expected_xano_instance,
        xano_workspace="Shop Service",
        backendgroup="Shop API",
        xano_canonical="shop-api",
        xano_host=expected_xano_host,
    )
    call4 = mocker.call(
        xano_instance=expected_xano_instance,
        xano_workspace="Warranty Service",
        backendgroup="Warranty API",
        xano_canonical="warranty-api",
        xano_host=expected_xano_host,
    )

    frontend_sync_mock.assert_has_calls([call2, call1, call3, call4], any_order=True)

    #assert call1 in frontend_sync_mock.call_args_list
    #assert call2 in frontend_sync_mock.call_args_list
    #assert call3 in frontend_sync_mock.call_args_list
    #assert call4 in frontend_sync_mock.call_args_list

def atest_filter():
    group_workspaces = {
        'User Service': ['Authentication', 'User Management'],
        'Shope Service': ['Shop API'],
        'Warranty Service': ['Warranty API']
    }
    backend = BackendAPI(_type="group", workspaces=group_workspaces, _filter=True)
    workspaces_from_net = backend.get_workspaces_from_network()
    filtered_workspaces = backend.get_workspaces()
    expected_workspace_names = ['User Service', 'Shop Service', 'Warranty Service']

    assert [ws['name'] for ws in filtered_workspaces] == expected_workspace_names
    #assert [ws['name'] for ws in filtered_workspaces] != workspaces_from_net

def test_filter(mocker):

    group_workspaces = {
        'User Service': ['Authentication', 'User Management'],
        'Shop Service': ['Shop API'],
        'Warranty Service': ['Warranty API']
    }




    get_ws_from_network = {
        'User Service': [{
            'id': 280,
            'name': 'Authentication',
            'description': '',
            'canonical': 'authentication',
            'swagger': False,
            'branch': 'v1'
        }, {
            'id': 244,
            'name': 'User Management',
            'description': 'This API group contains APIs that let you query cross instance data',
            'canonical': 'user-management',
            'swagger': False,
            'branch': 'v1'
        }],
        'Shop Service': [{
            'id': 244,
            'name': 'Shop API',
            'description': 'This API group contains APIs that let you query cross instance data',
            'canonical': 'shop-api',
            'swagger': False,
            'branch': 'v1'
        }],
        'Warranty Service': [{
            'id': 244,
            'name': 'Warranty API',
            'description': 'This API group contains APIs that let you query cross instance data',
            'canonical': 'warranty-api',
            'swagger': False,
            'branch': 'v1'
        }]
    }

    get_ws_from_network_mock = mocker.patch.object(BackendAPI, "get_workspaces_from_network", return_value=get_ws_from_network)

    backend = BackendAPI(_type="group", workspaces=group_workspaces, _filter=True)
    filtered_workspaces = backend.get_workspaces()


    backend.get_workspaces(enrich_with_apigroups=False)


    assert filtered_workspaces == get_ws_from_network_mock
>>>>>>> Stashed changes
