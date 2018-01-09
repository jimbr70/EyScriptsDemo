from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow


def main():
    sandbox = Sandbox()
    DefaultSetupWorkflow().register(sandbox, enable_configuration=False)
    sandbox.workflow.add_to_configuration(function=azure_app_extention,components=sandbox.components.apps)
    sandbox.execute_setup()


def azure_app_extention(sandbox, components):
    resource = sandbox.automation_api.GetResourceDetails("Globals_Resource")

    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='Reading data from globals resource')

    tfs_password = next((c.Value for c in resource.ResourceAttributes if (c.Name == "TFS_Password")), None)
    decrypt_password = sandbox.automation_api.DecryptPassword(tfs_password).Value
    tfs_uname = next((c.Value for c in resource.ResourceAttributes if (c.Name == "TFS_User")), None)

    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='Uname {0} and pword {1} found '.format(uname,decrypt_password))

    #Configure Azure apps
    azure_apps = sandbox.components.get_apps_by_name_contains('Azure')
    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='{0} Azure apps found '.format(len(azure_apps)))

    for app in azure_apps:
        #inject rsvnID, user name and password to the repo
        sandbox.apps_configuration.set_config_param(app=app,key='reservation_id',value=sandbox.id)
        sandbox.apps_configuration.set_config_param(app=app,key='qspword',value=decrypt_password)
        sandbox.apps_configuration.set_config_param(app=app,key='qsuname',value=uname)
        sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,message='AzureFromMarket')

    sandbox.apps_configuration.apply_apps_configurations(azure_apps)
    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,message='Finished configuring Azure apps')

main()









