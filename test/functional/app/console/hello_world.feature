Feature: Hello World
I need to be able to run hello world command

    Scenario: Run "app:hello_world" without arguments
        When I run the command "app:hello_world"
        Then print stdout
        And the command exit code should be 2
        And the stdout should contain:
        """
        [MissingArguments]
        Missing required arguments: required_arg
        """

    Scenario: Run "app:hello_world" without arguments
        When I run the command "app:hello_world" with arguments:
        """
        --option
        opt
        lala
        lele
        """
        Then print stdout
        And the command exit code should be 0
        And the stdout should contain:
        """
        Hello World
        required_arg lala
        non_required_arg lele
        option opt
        """
        And the file "var/hello_world" should contain:
        """
        required_arg lala
        non_required_arg lele
        option opt
        """
