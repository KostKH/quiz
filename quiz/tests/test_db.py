from tests.conftest import BASE_DIR


def test_check_migration_file_exist():
    app_dirs = [directory.name for directory in BASE_DIR.iterdir()]
    assert 'alembic' in app_dirs, (
        'В корневой директории не обнаружена папка `alembic`.'
    )
    alembic_dir = BASE_DIR / 'alembic'
    version_dir = [directory.name for directory in alembic_dir.iterdir()]
    assert 'versions' in version_dir, (
        'В папке `alembic` не обнаружена папка `versions`'
    )
    versions_dir = alembic_dir / 'versions'
    files_in_version_dir = [
        file.name for file in versions_dir.iterdir()
        if file.is_file() and '__init__' not in file.name
    ]
    assert len(files_in_version_dir) > 0, (
        'В папке `alembic.versions` не обнаружены файлы миграций'
    )
