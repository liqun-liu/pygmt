"""
Tests colorbar.
"""
import pytest
from pygmt import Figure


@pytest.mark.mpl_image_compare
def test_colorbar_box():
    """
    Create colorbar with box around it.
    """
    fig = Figure()
    fig.colorbar(cmap="rainbow", box=True, position="x0c/0c+w1c/0.5c")
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_box_with_fill():
    """
    Create colorbar with box that has a different colored fill.
    """
    fig = Figure()
    fig.colorbar(cmap="rainbow", box="+gorange", position="x0c/0c+w1c/0.5c")
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_truncated_to_zlow_zhigh():
    """
    Create colorbar truncated to z-low and z-high.
    """
    fig = Figure()
    fig.colorbar(cmap="rainbow", truncate=[0.15, 0.85], position="x0c/0c+w2c/0.5c")
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_scaled_z_values():
    """
    Create colorbar with z-values scaled to 0.1x of the original CPT.
    """
    fig = Figure()
    fig.colorbar(cmap="rainbow", scale=0.1, position="x0c/0c+w2c/0.5c")
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_shading_boolean():
    """
    Create colorbar and set shading with a Boolean value.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 10], projection="X15c", frame="a")
    fig.colorbar(cmap="geo", shading=True, frame=True)
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_shading_list():
    """
    Create colorbar and set shading by passing the high/low values as a list.
    """
    fig = Figure()
    fig.basemap(region=[0, 10, 0, 10], projection="X15c", frame="a")
    fig.colorbar(cmap="geo", shading=[-0.7, 0.2], frame=True)
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_frame_parameters():
    """
    Create colorbar with arguments for xlabel, ylabel, and annotation, and no
    argument passed to frame.
    """
    fig = Figure()
    fig.colorbar(
        cmap="rainbow",
        position="x0c/0c+w1c/0.5c",
        xlabel="test-x",
        ylabel="test-y",
        annotation=0.25,
    )
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_frame_list_parameters():
    """
    Create colorbar with a list passed to frame and an argument passed to
    xlabel.
    """
    fig = Figure()
    fig.colorbar(
        cmap="rainbow",
        position="x0c/0c+w1c/0.5c",
        frame=["a.25", "y+lylabel"],
        xlabel="test-x",
    )
    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_frame_string_parameters():
    """
    Create colorbar with a string passed to frame and arguments passed to
    xlabel and ylabel.
    """
    fig = Figure()
    fig.colorbar(
        cmap="rainbow",
        position="x0c/0c+w1c/0.5c",
        frame="a.5",
        xlabel="test-x",
        ylabel="test-y",
    )
    return fig
