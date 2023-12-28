from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard

class CustomAppIndexDashboard(AppIndexDashboard):
    def init_with_context(self, context):
        self.available_apps = self.get_admin_site().get_app_list(context)

class CustomDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        # Add modules to the dashboard
        self.children.append(modules.ModelList('Models', models=('your_app.models.*',)))
        # Add more modules as needed