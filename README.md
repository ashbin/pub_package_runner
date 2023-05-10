# pub_package_runner
A python script to run example project of pub.dev packages
</br>
This script can be used to launch the example project from pub.dev packages. 
The script will clone the package repository with depth=1, then launch Android Studio or Visual Studio Code (specified with -s argument) with example project.
Then run flutter run command from example directory

## Steps to run
1. Clone this repository to Downloads
2. cd ~/Downloads/pub_package_runner
3. ```python3 pub_package_runner.py <package-name> -s <path-to-android-studio> -f <path-to-flutter>```
</br> 

### Example 
``` python3 pub_package_runner.py scrollable_table_view  -s /Applications/Android\ Studio.app -f /Users/ashbin/fvm/versions/3.7.3/bin/flutter ```


Requirements : python3

Note : This script is tested with MacOS and python3 with popular flutter packages. 
