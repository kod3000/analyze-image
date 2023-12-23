import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ImageUploadService } from './image-upload.service';
import { HttpClient } from '@angular/common/http';

describe('ImageUploadService', () => {
  let service: ImageUploadService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ImageUploadService]
    });

    service = TestBed.inject(ImageUploadService);
    httpTestingController = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTestingController.verify();
  });

  it('should upload image and return expected response', () => {
    const testImage = new File([''], 'test-image.jpg', { type: 'image/jpeg' });
    const expectedResponse = 'some response';

    service.uploadImage(testImage).subscribe(response => {
      expect(response).toEqual(expectedResponse);
    });

    const req = httpTestingController.expectOne('http://localhost:8000/api/images/analyze-image');
    expect(req.request.method).toEqual('POST');
    expect(req.request.body.get('uploaded_file')).toEqual(testImage);
    req.flush(expectedResponse);
  });
});
