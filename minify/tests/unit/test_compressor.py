from mox import Mox
from minify import compressor

def test_js_compressor_can_be_run():
    mox = Mox()
    
    mox.StubOutWithMock(compressor,'jsmin')
    
    jscompress = compressor.JsCompressor("should-be-files", "should-be-file-output", "should-be-media-dir/")    

    mox.StubOutWithMock(jscompress,'get_merged_files', use_mock_anything=True)
    mox.StubOutWithMock(jscompress,'write_file', use_mock_anything=True)

    jscompress.get_merged_files().AndReturn("should-be-merged-files")
    compressor.jsmin("should-be-merged-files").AndReturn("should-be-content-compressed")


    jscompress.write_file("should-be-content-compressed", "should-be-media-dir/should-be-file-output")
    
    mox.ReplayAll()
    try:
        jscompress.run()
        
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_css_compressor_can_be_run():
    mox = Mox()
    
    mox.StubOutWithMock(compressor,'CssMin', use_mock_anything=True)
    
    compress = compressor.CssCompressor("should-be-files", "should-be-file-output", "should-be-media-dir/")    

    mox.StubOutWithMock(compress,'get_merged_files', use_mock_anything=True)
    mox.StubOutWithMock(compress,'write_file', use_mock_anything=True)

    compress.get_merged_files().AndReturn("should-be-merged-files")

    cssmin_mock = mox.CreateMockAnything()
    cssmin_mock.compress("should-be-merged-files").AndReturn("should-be-content-compressed")
    compressor.CssMin().AndReturn(cssmin_mock)
    
    compress.write_file("should-be-content-compressed", "should-be-media-dir/should-be-file-output")
    
    mox.ReplayAll()
    try:
        compress.run()
        
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()        
