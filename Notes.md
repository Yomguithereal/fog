# Notes

# CLI Commands

* Take piped input.
* `--inplace`

## transform

* Decimals
* Scientific notation resolver

```
transform file column trim,squeeze,upper,lower
--to <new-column-name>
```

## rename

rename + add-headers => xsv?

```
rename file col1,col2 col1,col2
```

## split

Also need the inverse (ex: mat1, mat2, mat3) blank or not

```
split file col
--separator "|"
```

## unique

```
unique file col1,col2
```

## flag

```
flag file col pattern
```
