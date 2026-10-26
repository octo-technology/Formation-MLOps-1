setup() {
    cd "$BATS_TEST_DIRNAME"
}

@test "titanic notebook runs without errors" {
    # Execute a copy so that training does not overwrite the repository's models.
    mkdir -p "$BATS_TEST_TMPDIR/notebook" "$BATS_TEST_TMPDIR/models"
    cp notebook/titanic.ipynb "$BATS_TEST_TMPDIR/notebook/"
    ln -s "$BATS_TEST_DIRNAME/input" "$BATS_TEST_TMPDIR/input"
    run uv run jupyter nbconvert --to notebook --execute \
        "$BATS_TEST_TMPDIR/notebook/titanic.ipynb" \
        --output executed --output-dir "$BATS_TEST_TMPDIR"
    [ "$status" -eq 0 ]
}

@test "unit tests are green" {
    run uv run python -m pytest
    [ "$status" -eq 0 ]
}

@test "we are able to build the python package" {
    run uv build --out-dir "$BATS_TEST_TMPDIR/dist"
    [ "$status" -eq 0 ]
}

@test "build the documentation" {
    run uv run sphinx-build -W -b html docs "$BATS_TEST_TMPDIR/html"
    [ "$status" -eq 0 ]
}
