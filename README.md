# AndroidStringFormatValidator

The localizations of Android strings from crowdsourcing platform might break the string formatters. 

** Example: **
```xml
<!-- value/strings.xml -->
<string name="sample_text">sample text with format: %s</string>
	
<!-- value-es/strings.xml -->
<string name="sample_text">sample text with format: % s</string>
```
The %s formatting characters are broken after tranlsation. To identify such erros before releasing build, we can just add a custom gradle task, checkString, before the preBuild stage of the assemble task. 

Ｗith the custom "checkString" task, the errors would be identified and displayed with the build ouput log: 

    Executing tasks: [assemble] in project /Users/kennylee/code/Github/AndroidStringFormatValidator

    > Task :app:checkString FAILED

    FAILURE: Build failed with an exception.

    * Where:
    Build file '/Users/kennylee/code/Github/AndroidStringFormatValidator/app/build.gradle' line: 49

    * What went wrong:
    Execution failed for task ':app:checkString'.
    > !!!! ERROR !!!! 
      File: /Users/kennylee/code/Github/AndroidStringFormatValidator/app/src/main/res/values/strings.xml 
      Invalid format code detected: sample_text % 

    * Try:
    Run with --stacktrace option to get the stack trace. Run with --info or --debug option to get more log output. Run with --scan to get full insights.

    * Get more help at https://help.gradle.org

    BUILD FAILED in 0s
    1 actionable task: 1 executed
    00:11:03: Task execution finished 'assemble'.
