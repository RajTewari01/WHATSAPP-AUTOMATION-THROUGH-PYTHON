from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
import os
from urllib.parse import quote
from kivy.utils import platform


class PasswordApp(MDApp):
    def build(self):
        return Builder.load_file("password.kv")

    def generate_credentials(self):
        service_name = self.root.ids.service.text
        username = self.root.ids.username.text
        password = self.root.ids.password.text
        message = f"Service: {service_name}\nUsername: {username}\nPassword: {password}"

        # Save credentials locally
        path = os.path.join(self.user_data_dir, "credentials.txt")
        with open(path, "a") as f:
            f.write(f"{service_name} -> {username} | {password}\n")

        # Only run on Android
        if platform == "android":
            try:
                from jnius import autoclass, cast
                Intent = autoclass("android.content.Intent")
                Uri = autoclass("android.net.Uri")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")

                encoded = quote(message)
                phone_number = "911234567890"  # change this to your WhatsApp number
                uri = Uri.parse(f"whatsapp://send?phone={phone_number}&text={encoded}")
                intent = Intent(Intent.ACTION_VIEW)
                intent.setData(uri)

                currentActivity = cast("android.app.Activity", PythonActivity.mActivity)
                currentActivity.startActivity(intent)

            except Exception as e:
                print("WhatsApp send failed:", e)


if __name__ == "__main__":
    PasswordApp().run()