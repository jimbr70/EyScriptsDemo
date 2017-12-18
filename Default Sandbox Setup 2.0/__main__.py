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
    # application_server_address = sandbox.components.get_apps_by_name_contains('Application')[0].deployed_app.FullAddress

    azure_from_market_apps = sandbox.components.get_apps_by_name_contains('azurefrommarket')
    #REBOT ALL APPS
    # power off
    # power on


    # get uname and pword from the resource that keeps them
    # decrypt the password
    # execute the script woth the user anem and the password

    for app in azure_from_market_apps:
        sandbox.apps_configuration.set_config_param(app=app,
                                                    key='qspword',
                                                    value="pword1")

        sandbox.apps_configuration.set_config_param(app=app,
                                                    key='qsuname',
                                                    value="uname1")

        sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                               message='AzureApp configured')

    sandbox.apps_configuration.apply_apps_configurations(azure_from_market_apps)

    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='Finished to configure Azure apps')

main()


