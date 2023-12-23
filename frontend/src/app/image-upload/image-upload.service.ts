import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root',
})
export class ImageUploadService {
  constructor(private http: HttpClient) {}
  uploadImage(image: File): any {
    const formData = new FormData();
    formData.append('uploaded_file', image);
    return this.http.post('/api/images/analyze-image', formData, {
      responseType: 'text',
    });
  }
}
