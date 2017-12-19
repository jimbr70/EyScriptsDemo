from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow


def main():
    sandbox = Sandbox()
    DefaultSetupWorkflow().register(sandbox, enable_configuration=False)
    sandbox.workflow.add_to_configuration(function=azure_app_extention,components=sandbox.components.apps)
    sandbox.execute_setup()



def azure_app_extention(sandbox, components):
    resource = sandbox.automation_api.GetResourceDetails("qs_cred_resource")

    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='Reading data from qs resource')

    password = next((c.Value for c in resource.ResourceAttributes if (c.Name == "Password")), None)
    decrypt_password = sandbox.automation_api.DecryptPassword(password).Value
    uname = next((c.Value for c in resource.ResourceAttributes if (c.Name == "User")), None)

    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='Uname {0} and powrd {1} found '.format(uname,decrypt_password))

    #Configure Azure apps
    azure_from_market_apps = sandbox.components.get_apps_by_name_contains('AzureFromMarket')
    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='AzureFromMarket found {0}'.format(len(azure_from_market_apps)))

    for app in azure_from_market_apps:
        #inject user name and password to the repo
        sandbox.apps_configuration.set_config_param(app=app,key='qspword',value=decrypt_password)
        sandbox.apps_configuration.set_config_param(app=app,key='qsuname',value=uname)
        sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,message='AzureFromMarket')

    sandbox.apps_configuration.apply_apps_configurations(azure_from_market_apps)
    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,message='Finished configuring Azure apps')

main()









