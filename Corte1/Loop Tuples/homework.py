{"nbformat":4,"nbformat_minor":0,"metadata":{"colab":{"provenance":[],"authorship_tag":"ABX9TyMZpSazxT6zd14qL0VPljmB"},"kernelspec":{"name":"python3","display_name":"Python 3"},"language_info":{"name":"python"}},"cells":[{"cell_type":"code","execution_count":1,"metadata":{"id":"2KPZxTeElkie","executionInfo":{"status":"ok","timestamp":1724893830601,"user_tz":300,"elapsed":21069,"user":{"displayName":"Jose Ardila","userId":"07434960911335861001"}},"outputId":"0e1fd647-dc1e-415d-fa59-4d0f77644de5","colab":{"base_uri":"https://localhost:8080/"}},"outputs":[{"output_type":"stream","name":"stdout","text":["Enter a number: 2\n","Enter a number: 7\n","Different\n","Type of a is <class 'int'>\n","Type of b is <class 'float'>\n","c= 9.0\n","a and b are of different types\n"]}],"source":["a = input(\"Enter a number: \")\n","a = int(a)\n","b = input(\"Enter a number: \")\n","b = float(b)\n","c= a + b\n","\n","if a == b:\n","  print(\"equal\")\n","else:\n","  print(\"Different\")\n","\n","print(\"Type of a is\", type(a))\n","print(\"Type of b is\", type(b))\n","print(\"c=\", c)\n","\n","if type(a) == type(b):\n","  print(\"a and b are of the same type\")\n","else:\n","  print(\"a and b are of different types\")\n"]}]}