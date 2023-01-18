@test "titanic notebook run without problem" {
    conda source python_indus
	mkdir models
	jupyter nbconvert --to script notebook/titanic.ipynb
	cd notebook
	run python titanic.py
	[ "$status" -eq 0 ]
}


@test "unit tests are green" {
        run pytest tests
        [ "$status" -eq 0 ]
}


@test "we are able to build the python package" {
        run python3 setup.py sdist bdist_wheel
	[ "$status" -eq 0 ]
}


@test "build the documentation" {
        run sphinx-build -b html docs docs/_build
	[ "$status" -eq 0 ]
}



teardown() {
	rm -r -r models/
	rm -r -f build/
	rm -r -f dist/
	rm -r -f docs/_build/.buildinfo
	rm -r -f docs/_build/.doctrees/
	rm -r -f docs/_build/_sources/
	rm -r -f docs/_build/_static/
	rm -f docs/_build/genindex.html
	rm -f docs/_build/index.html
	rm -f docs/_build/objects.inv
	rm -f docs/_build/search.html
	rm -f docs/_build/searchindex.js
	rm -r -f formation_indus_ds.egg-info/
	rm -f notebook/Predict notebook.py
	rm -f notebook/titanic.py
	rm -f notebook/y_test15.csv
	rm -r -f src/__pycache__/
	rm -r -f tests/__pycache__/
	rm -r -f docs/_build/_sources/
	rm -r -f notebook/Predict\ notebook.py
}

