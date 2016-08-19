# pytest-unmark

Side project to see if I could have an `unmark`, that would remove marks that were applied from a greater scope. 



Example:


```py

@pytest.mark.long
class TestMe(object):
  def test_one(self):
    assert True
    
  @pytest.unmmark.long
  def test_two(self):
    assert True
    
```

Run via `py.test -m long` should only run `test_one`. 
