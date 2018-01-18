from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow


def main():
    sandbox = Sandbox()
    DefaultSetupWorkflow().register(sandbox, enable_configuration=False)
    sandbox.workflow.add_to_configuration(function=azure_app_extention, components=sandbox.components.apps)
    sandbox.execute_setup()


def azure_app_extention(sandbox, components):
    """
    :param Sandbox sandbox:
    :param components:
    :return:
    """
    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='Reading data from globals resource')
    resource = sandbox.automation_api.GetResourceDetails("Globals_Resource")
    sandbox.logger.debug("Retrieved 'Globals_Resource' resource. Attributes:")
    sandbox.logger.info(" ; ".join(["Name: " + att.Name + ", Value: " + att.Value for att in resource.ResourceAttributes]))

    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='Processing TFS data')
    # TFS
    tfs_password = next((c.Value for c in resource.ResourceAttributes if (c.Name == "TFS_Password")), None)
    tfs_decrypted = sandbox.automation_api.DecryptPassword(tfs_password).Value
    tfs_uname = next((c.Value for c in resource.ResourceAttributes if (c.Name == "TFS_User")), None)
    sandbox.logger.info("TFS_User: {0}".format(tfs_uname))

    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='Processing FTP srvr data')
    # FTP
    ftp_server = next((c.Value for c in resource.ResourceAttributes if (c.Name == "FTP_Server")), None)
    sandbox.logger.info("FTP_Server: {0}".format(ftp_server))

    ftp_password = next((c.Value for c in resource.ResourceAttributes if (c.Name == "FTP_Password")), None)
    ftp_decrypted = sandbox.automation_api.DecryptPassword(ftp_password).Value
    ftp_uname = next((c.Value for c in resource.ResourceAttributes if (c.Name == "FTP_User")), None)
    sandbox.logger.info("FTP_User: {0}".format(ftp_uname))

    ftp_hostkey = next((c.Value for c in resource.ResourceAttributes if (c.Name == "FTP_Hostkey")), None)
    sandbox.logger.info("FTP_Hostkey: {0}".format(ftp_hostkey))

    qsscript1_url = next((c.Value for c in resource.ResourceAttributes if (c.Name == "PSFTP_TFS_Link")), None)
    sandbox.logger.info("FTP_Hostkey: {0}".format(qsscript1_url))

    # Configure Azure apps
    azure_apps = sandbox.components.get_apps_by_name_contains('azure')
    sandbox.logger.info("Found {0} apps".format(len(azure_apps)))
    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='{0} Azure apps found '.format(len(azure_apps)))

    for app in azure_apps:
        sandbox.logger.info("Setting config params for deployed app '{0}' (app request: '{1}')"
                            .format(app.deployed_app.Name, app.app_request.app_resource.Name))
        sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id, message=app.deployed_app.Name)

        # inject rsvnID, TFS, and FTP meta data to the app definition
        sandbox.apps_configuration.set_config_param(app=app, key='reservation_id', value=sandbox.id)
        sandbox.apps_configuration.set_config_param(app=app, key='qspword', value=tfs_decrypted)
        sandbox.apps_configuration.set_config_param(app=app, key='qsuname', value=tfs_uname)

        sandbox.apps_configuration.set_config_param(app=app, key='ftpsrvr', value=ftp_server)
        sandbox.apps_configuration.set_config_param(app=app, key='ftpuser', value=ftp_uname)
        sandbox.apps_configuration.set_config_param(app=app, key='ftppass', value=ftp_decrypted)
        sandbox.apps_configuration.set_config_param(app=app, key='ftphostkey', value=ftp_hostkey)
        sandbox.apps_configuration.set_config_param(app=app, key='qsscript1_url',value=qsscript1_url)

    sandbox.apps_configuration.apply_apps_configurations(azure_apps)
    sandbox.automation_api.WriteMessageToReservationOutput(reservationId=sandbox.id,
                                                           message='Setup finished configuring Azure apps')


main()
