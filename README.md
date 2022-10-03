# argo-probe-xml

The package contains the generic `check_xml` probe which remotely checks XML. It can check if XML contains nodes with given XPaths, and it also has a possibility to validate those values. Furthermore, the probe can check multiple nodes of the same XML document at the same time.

## Synopsis

### Required arguments

The probe has two required arguments: 

* `-u`, `--url` which is the URL of the XML document we wish to inspect,
* `-t`, `--timeout` which is the time in seconds after which the connection will time out.

### Optional arguments

In addition to the three mandatory arguments, probe also has six optional:

* `-x`, `--xpath` which is XPath for the node we wish to inspect; this one can also be provided as a space separated list of multiple XPaths for multiple nodes we wish to inspect in the same document,
* `--ok` node value which will return OK status; each other value will return critical
  * in case there are multiple nodes with the same XPath, the probe will return OK status only if all the nodes' values are equal to the value provided by the argument,
  * in case there are multiple nodes with the same XPath, the probe will return WARNING status if some (but not all!) of the nodes' values are equal to the value provided by the argument,
  * in case there are multiple nodes with the same XPath, the probe will return CRITICAL status if none of the nodes' values is equal to the value provided by the argument,
* `-w`, `--warning` - values' warning range; the probe will return WARNING status if the node value is outside the given range; the range format is given in the table below
* `-c`, `--critical` - values' critical range; the probe will return CRITICAL status if the node value is outside the given range; the range format is the same as for the `-w` argument
* `--age` age in hours; this one is used for checking that nodes with time entries have age less than the one given; the age is calculated using the UTC time of time of probe execution
* `--time-format` time format used by Python datetime library; this argument is mandatory when `--age` is used; if the time is given as a UNIX timestamp, then `UNIX` should be used as value of this argument
 
| Range definition | The probe returns |
| --- | --- |
| 10 | Probe raises alert when value is outside of [0, 10] range |
|10: | Probe raises alert when value is outside of [10, &infin;] range |
|10:20| Probe raises alert when value is outside of [10, 20] range |
|@10:20| Probe raises alert when value is inside the [10, 20] range (@ means negation)|

#### Note

Since the probe can accept multiple XPaths to inspect multiple nodes, we can also enter multiple values for each of the optional arguments (except the `--time-format` - it is assumed that it is the same for the entire document). In that case, you must provide arguments' values as a space separated list, but each element must have a prefix of the form `<node_name>:`. In case it is missing, the probe will raise an error. If only one XPath is provided to the probe, this prefix is not necessary.

Optional arguments `-w` and `-c` can be used together, but all the rest cannot be combined (with the exception of `--time-format`, which **must** be used with argument `--age`). E.g. when using `--ok`, we cannot use `-w`, `-c` or `--age` for the same XPath (they can be used for different XPaths). We can use `-c` and `-w` for the same node, but if we do use any of those two, we cannot use `--ok` or `--age` for the same node.


## Examples

Checking that XML document is valid

```
# /usr/libexec/argo/probes/xml/check_xml -u https://xml.argo.eu/ -t 30 
OK - Response OK
```

Checking that XML document contains node with XPath `/root/test/path`

```
# /usr/libexec/argo/probes/xml/check_xml -u https://xml.argo.eu/ -t 30 -x /root/test/path
OK - Node with XPath '/root/test/path' found
```

Checking that XML documents contains nodes with XPaths `/root/test/path1` and `/root/test/path2`

```
# /usr/libexec/argo/probes/xml/check_xml -u https://xml.argo.eu/ -t 30 -x /root/test/path1 /root/test/path2
OK - All the checks pass
```

Checking that the node has a certain value

```
# /usr/libexec/argo/probes/xml/check_xml -u https://xml.argo.eu/ -t 30 -x /root/test/path --ok is_ok
OK - /root/test/path: All the node(s) values equal to 'is_ok'
```

Validating values of multiple nodes differently

```
# /usr/libexec/argo/probes/xml/check_xml -u https://xml.argo.eu/ -t 30 -x /root/test/path1 /root/test/path2 -w path1:10:20 -c path1:20:30 --age path2:3 --time-format %Y-%m-%d-%H:%M:%S
OK - All the checks pass
```
