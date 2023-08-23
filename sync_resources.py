class FrontendAPI:

    def __init__(self, _type="mywork"):
        self.resources = self.list_resources()
        self.environments = self.list_environments()

    def list_resources(self):  # from network, mock this
        # return test resources from retool
        return [
            {
                'id': '1',
                'type': 'restapi',
                'display_name': 'Garancija'
            }, {
                'id': '2',
                'type': 'restapi',
                'display_name': 'User'
            }, {
                'id': '3',
                'type': 'restapi',
                'display_name': 'Shop'
            }
        ]

    def get_retool_resource_name(self, xano_instance, xano_workspace, backendgroup, xano_canonical):
        return f"{xano_instance} / {xano_workspace} / {backendgroup} ({xano_canonical})"

    def list_environments(self):  # from network, but do not mock this
        # return test environments from retool
        return [
            {
                'id': '1',
                'name': 'staging',
                'color': '#E9AB11',
                'default': False
            }, {
                'id': '2',
                'name': 'production',
                'color': '#3C92DC',
                'default': True
            }
        ]

    def get_environment(self, environment_name):
        return [x for x in self.environments if x['name'] == environment_name][0]

    def update_existing_configuration(self):
        # ovde se kao nesto desava, ovo treba da se mokuje i assertuje

        pass

    def sync_new_configuration(self):
        # ovde se kao nesto desava, ovo treba da se mokuje i assertuje
        pass

    def sync_single_configuration(self, resource, configurations, environment_name, base_url, headers):
        conf = [x['environment'] for x in configurations if x['environment']['name'] == environment_name]

        if conf:
            conf = conf[0]
            # Make sure that configuration is correct, and if it's not update it
            try:

                # THIS IS NOT A TEST
                expected_headers = headers
                actual_headers = conf['options']['headers']

                for header in expected_headers:
                    assert header in actual_headers

                for header in actual_headers:
                    assert header in expected_headers

                print(f"Skipped {environment_name}")
            except AssertionError:
                # Update existing configuration
                self.update_existing_configuration()
                print(f"Updated {environment_name}")
        else:
            # create new configuration
            self.sync_new_configuration()
            print(f"Created {environment_name}")

    def test_method_raises_exception(self, x):
        if x < 5:
            raise Exception("Manje od pet")
        else:
            return x

    def get_configurations_from_network(self):  # ne morate da mokujete ovo
        return [
            {
                "environment": {
                    "name": "staging",
                    "options": {
                        "headers": [["x-data-source", "test"], ["content-type", "application/json"]],
                    }
                }
            },
            {
                "environment": {
                    "name": "production",
                    "options": {
                        "headers": [["x-data-source", "live"], ["content-type", "application/json"]],
                    }
                }
            }
        ]

    def sync_configurations(self, resource, xano_canonical, xano_host):
        configurations = self.get_configurations_from_network()

        self.sync_single_configuration(
            resource=resource,
            configurations=configurations,
            environment_name="staging",
            base_url=f"{xano_host}/api:{xano_canonical}",
            headers=[["x-data-source", "test"], ["content-type", "application/json"]],
        )
        self.sync_single_configuration(
            resource=resource,
            configurations=configurations,
            environment_name="production",
            base_url=f"{xano_host}/api:{xano_canonical}",
            headers=[["x-data-source", "live"], ["content-type", "application/json"]],
        )

    def sync_new_resource(self, xano_instance, xano_workspace, backendgroup, xano_canonical, xano_host):
        name = self.get_retool_resource_name(
            xano_instance=xano_instance,
            xano_workspace=xano_workspace,
            backendgroup=backendgroup,
            xano_canonical=xano_canonical,
        )
        resource = {

        }
        print("Created")

        self.sync_configurations(
            resource,
            xano_canonical,
            xano_host
        )

    def sync_resource_name(self, resource):
        pass

    def sync_existing_resource(self, resource, xano_instance, xano_workspace, backendgroup, xano_canonical, xano_host):

        name = self.get_retool_resource_name(
            xano_instance=xano_instance,
            xano_workspace=xano_workspace,
            backendgroup=backendgroup,
            xano_canonical=xano_canonical,
        )
        if resource['display_name'] != name:
            print(f"Updated name")
            self.sync_resource_name(resource)
        else:
            pass

        self.sync_configurations(
            resource,
            xano_canonical,
            xano_host
        )

    def sync(self, xano_instance, xano_workspace, backendgroup, xano_canonical, xano_host):
        existing_resource = None
        for resource in self.resources:
            if f"({xano_canonical})" in resource['display_name']:
                existing_resource = resource

        name = self.get_retool_resource_name(
            xano_instance=xano_instance,
            xano_workspace=xano_workspace,
            backendgroup=backendgroup,
            xano_canonical=xano_canonical,
        )
        print(name)

        if existing_resource:
            self.sync_existing_resource(
                resource=existing_resource,
                xano_instance=xano_instance,
                xano_workspace=xano_workspace,
                backendgroup=backendgroup,
                xano_canonical=xano_canonical,
                xano_host=xano_host
            )
        else:
            self.sync_new_resource(
                xano_instance=xano_instance,
                xano_workspace=xano_workspace,
                backendgroup=backendgroup,
                xano_canonical=xano_canonical,
                xano_host=xano_host
            )

        print("=====================================")
        print("=====================================")


class BackendAPI:

    CONFIG = {
        'group': {
            "base_url": "https://ivn-consulting.com/group",
            "name": "GROUP",
            "token": "group_token",
        },
        'prod': {
            "base_url": "https://ivn-consulting.com/prod",
            "name": "PROD",
            "token": "prod_token",
        },
    }

    def __init__(self, _type, workspaces, _filter):
        self.type = _type
        self.name = self.CONFIG[_type]['name']
        self.host = self.CONFIG[_type]['base_url']
        self.token = self.CONFIG[_type]['token']
        self.workspaces = workspaces
        self._filter = _filter

    def get_workspaces_from_network(self):
        return [
            {'id': 14,
             'name': 'User Service',
             'description': '',
             'branch': 'v1',
             'apigroups': [
                 {
                     'id': 24,
                     'name': 'Authentication',
                     'description': '',
                     'canonical': 'authentication',
                     'swagger': False
                 }, {
                     'id': 25,
                     'name': 'User Management',
                     'description': '',
                     'canonical': 'user-management',
                     'swagger': False
                 }, {
                     'id': 26,
                     'name': 'Something else',
                     'description': '',
                     'canonical': 'something else',
                     'swagger': False
                 }
             ]}, {'id': 15,
             'name': 'Shop Service',
             'description': '',
             'branch': 'v1',
             'apigroups': [
                 {
                     'id': 24,
                     'name': 'Shop API',
                     'description': '',
                     'canonical': 'shop-api',
                     'swagger': False
                 }, {
                     'id': 25,
                     'name': 'User Management',
                     'description': '',
                     'canonical': 'user-management',
                     'swagger': False
                 }
             ]}, {'id': 16,
             'name': 'Warranty Service',
             'description': '',
             'branch': 'v1',
             'apigroups': [
                 {
                     'id': 24,
                     'name': 'Warranty API',
                     'description': '',
                     'canonical': 'shop-api',
                     'swagger': False
                 }, {
                     'id': 25,
                     'name': 'User Management',
                     'description': '',
                     'canonical': 'user-management',
                     'swagger': False
                 }
             ]}
        ]

    def get_workspaces(self, enrich_with_apigroups=False):
        data = self.get_workspaces_from_network()
        if self._filter:
            data = [x for x in data if x['name'] in self.workspaces.keys()]
        if enrich_with_apigroups:
            self.enrich_with_apigroups(workspaces=data)
        return data

    def get_apigroups_from_network(self):
        return {
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

    def enrich_with_apigroups(self, workspaces):
        test_data = self.get_apigroups_from_network()
        for workspace in workspaces:
            data = test_data[workspace['name']]
            if self._filter:
                """data = [x for x in data if x['name'] in self.workspaces.get(workspace['name'], [])]
                star_filter
                [x for x in data if x in self.workspaces.get(workspace['name'], []) == '*']
                data = [x for x in data if "*" in self.workspaces.get(workspace['name'], [])]
                workspace['apigroups'] = data

                data = [x for x in data if "*" in self.workspaces.get(workspace['name'], [])]
                workspace['apigroups'] = data"""
                if '*' in self.workspaces.get(workspace['name'], []):
                    workspace['apigroups'] = data
                else:
                    data = [x for x in data if x['name'] in self.workspaces.get(workspace['name'], [])]
                    workspace['apigroups'] = data


class Syncer:

    def __init__(self, backend, frontend_api):
        self.backend = backend
        self.frontend_api = frontend_api

    def sync(self):
        workspaces = self.backend.get_workspaces(enrich_with_apigroups=True)
        #import pdb
        #pdb.set_trace()
        for workspace in workspaces:
            for api_group in workspace['apigroups']:
                self.frontend_api.sync(
                    xano_instance=self.backend.name,
                    xano_workspace=workspace['name'],
                    backendgroup=api_group['name'],
                    xano_canonical=api_group['canonical'],
                    xano_host=self.backend.host,
                )


if __name__ == "__main__":

    # Frontend
    group_workspaces = {
        'User Service': ['Authentication', 'User Management'],
        'Shop Service': ['Shop API'],
        'Warranty Service': ['Warranty API']
    }

    frontend = FrontendAPI(_type="myhome")
    backend = BackendAPI(_type="group", workspaces=group_workspaces, _filter=True)
    syncer = Syncer(backend=backend, frontend_api=frontend)
    workspaces = syncer.sync()
    print(workspaces)

