# Notes

# CLI Commands

* Take piped input.
* `--inplace`

## transform

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

Also need the inverse (ex: mat1, mat2, mat3)

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
