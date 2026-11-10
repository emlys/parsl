import os

import pytest

import parsl
from parsl.app.app import bash_app, python_app
from parsl.data_provider.files import File


@bash_app
def generate(outputs=(), stdout=parsl.AUTO_LOGNAME, stderr=parsl.AUTO_LOGNAME):
    return "echo 1 > {o} 2>&1".format(o=outputs[0])


@bash_app
def concat(inputs=(), outputs=(), stdout=None, stderr=None):
    return "cat {0} >> {1}".format(" ".join(map(lambda x: x.filepath, inputs)), outputs[0])


@python_app
def total(inputs=()):
    with open(inputs[0].filepath, "r") as f:
        return sum(int(line) for line in f)


@pytest.mark.staging_required
@pytest.mark.parametrize("width", (5, 10, 15))
def test_parallel_dataflow(tmpd_cwd, width):
    """Test parallel dataflow from docs on Composing workflows
    """
    output_files = []
    # create n files with the contents "1"
    # put each file in its own subdirectory to avoid a race condition on
    # Windows where creating a larger number files in the same directory
    # simultaneously would cause some to fail
    for i in range(width):
        subdir = tmpd_cwd / f"dir-{i}"
        os.makedirs(subdir)
        filepath = subdir / f"file-{i}.txt"
        filepath.touch()
        output_files.append(
            generate(outputs=[File(str(filepath))]))

    # concatenate the files into a single file
    cc = concat(
        inputs=[i.outputs[0] for i in output_files],
        outputs=[File(str(tmpd_cwd / "all.txt"))]
    )

    # calculate the sum of the numbers
    totals = total(inputs=[cc.outputs[0]])
    assert totals.result() == len(output_files)
