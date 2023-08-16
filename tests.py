from sync_resources import BackendAPI , FrontendAPI , Syncer
def setup():
    pass

def increment(i):
    print("izvrsio sam se")
    return i

def f():
    result = increment(123)
    return result


def test_f_with_spy(mocker):
    import tests
    increment_spy = mocker.spy(tests, 'increment')

    f()

    increment_spy.assert_called_once()


def test_f_calls_increment(mocker):
    # Given
    increment_mock = mocker.patch('tests.increment')

    # When
    f()

    # Then
    increment_mock.assert_called_once()


def test_f_values(mocker):
    # Given
    increment_mock = mocker.patch('tests.increment')
    increment_mock.return_value = 123

    # When
    actual_result = f()

    # Then
    assert actual_result == 123


def test_prvi(mocker):
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





def test_get_workspaces(mocker):

        #Given
        group_workspaces = {
        'a': ['Authentication', 'User Management'],
        'b': ['Shop API'],
        }

        get_wsfn_mock = mocker.patch.object(BackendAPI, "get_workspaces_from_network")
        get_wsfn_mock.return_value =[
            {'name': 'a'},
            {'name': 'b'},
            {'name': 'c'},
            {'name': 'd'},
            {'name': 'e'},
        ]
        backend = BackendAPI(_type="group", workspaces=group_workspaces, _filter=True)
        #When
        filtered_workspaces = backend.get_workspaces(enrich_with_apigroups=False)
        expected_workspaces = ["a", "b"]
        #Then
        print(group_workspaces)
        assert [ws["name"] for ws in filtered_workspaces] == expected_workspaces
