toplevel=$(git rev-parse --show-toplevel)
destination=${toplevel}/extension/pkg/src.xpi
zip -r $destination ${toplevel}/extension/src
echo $destination
