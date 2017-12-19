from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow


def main():
    sandbox = Sandbox()
    DefaultSetupWorkflow().register(sandbox, enable_configuration=False)
    sandbox.workflow.add_to_configuration(function=azure_app_extention)
    sandbox.execute_setup()



def azure_app_extention(sandbox, components):

    # resource = sandbox.automation_api.GetResourceDetails("qs_cred_resource")
    # password = next(iter(c for c in resource.ResourceAttributes if c == "password"), None)
    # sandbox.automation_api.DecryptPassword(password)
    # uname = next(iter(c for c in resource.ResourceAttributes if c == "uname"), None)


    #build_id = sandbox.global_inputs['build_id']

    # Configure web servers
    # application_server_address = sandbox.components.get_apps_by_name_contains('Application')[0].deployed_app.FullAddress

    azure_from_market_apps = sandbox.components.get_apps_by_name_contains('azurefrommarket')

    # get uname and pword from the resource that keeps them
    # decrypt the password
    # execute the script woth the user anem and the password

    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='Azure app from market found {0}'.format(len(azure_from_market_apps)))

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
                                                           message='Finished configuring Azure apps')

main()









