from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow


def main():
    sandbox = Sandbox()
    DefaultSetupWorkflow().register(sandbox, enable_configuration=False)
    sandbox.workflow.add_to_configuration(function=azure_app_extention)
    sandbox.execute_setup()


def azure_app_extention(sandbox, components):
    #build_id = sandbox.global_inputs['build_id']

    # Configure web servers
    application_server_address = sandbox.components.get_apps_by_name_contains('Application')[0].deployed_app.FullAddress

    web_servers = sandbox.components.get_apps_by_name_contains('Web')

    for app in web_servers:
        sandbox.apps_configuration.set_config_param(app=app,
                                                    key='Application Server',
                                                    value=application_server_address)

        sandbox.apps_configuration.set_config_param(app=app,
                                                    key='build_id',
                                                    value=build_id)

        sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                               message='AzureApp configured with build_id {0}, and Application Server address {1}'
                                                               .format(str(build_id), str(application_server_address)))

    sandbox.apps_configuration.apply_apps_configurations(web_servers)
    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='Finished to configure Web Servers')

main()


