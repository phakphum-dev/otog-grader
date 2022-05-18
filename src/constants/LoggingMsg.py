class Logging:
    noResult = f"""# Report of submission: <!subId!>

## Submission Info

**Submission Id** : `<!subId!>`

**User Id** : `<!userId!>`

**Lang** : `<!lang!>`

## Problem Info

**Problem Id** : `<!proId!>`

**Time limit** : `<!proSec!>s`

**Mem Limit** : `<!proMem!>mb`

## Result of problem <!proId!>

```<!lang!>
<!code!>
```

_result It's not done yet..._

"""
    afterResult = """

# Report of submission: <!subId!>

## Submission Info

**Submission Id** : `<!subId!>`

**User Id** : `<!userId!>`

**Lang** : `<!lang!>`

## Problem Info

**Problem Id** : `<!proId!>`

**Time limit** : `<!proSec!>s`

**Mem Limit** : `<!proMem!>mb`

## Result of problem <!proId!>

```<!lang!>
<!code!>
```

**Score** : `<!resScore!>`

**Result** : `<!resVerdict!>`

**TimeLen** : `<!resTime!>s`

**MemUse** : `<!resMem!>kb???`

**Comment**

```
<!resErrMsg!>
```

"""
