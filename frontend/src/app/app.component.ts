import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ImageUploadService } from './image-upload/image-upload.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  imageAnalysis: any[] = [];
  imageUrl: string = '';
data_loading: boolean = false;
  constructor(
    private imageUploadService: ImageUploadService,
    private snackBar: MatSnackBar
  ) {}

  onImageChange(event: Event): void {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;
    this.data_loading = true;
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = (e: ProgressEvent<FileReader>) => {
      this.imageUrl = e.target?.result as string;
    };

    this.imageUploadService.uploadImage(file).subscribe(
      (response:any) => this.handleResponse(response),
      (error:any) => this.handleError(error)
    );
  }

  private handleResponse(response: any): void {
    response = JSON.parse(response);

    if (response?.openai_response?.error) {
      this.addAnalysisResult(response, 'error', 'Your image uploaded but there was a problem with analyzing the content.');
      console.warn('This error is with using the wrong API key, please check that the flag is set correctly');
      this.data_loading = false;
      return;
    }

    this.addAnalysisResult(response, 'success', 'Your image was uploaded successfully');
    this.data_loading = false;
  }

  private handleError(error: any): void {
    error = JSON.parse(error);

    if (error?.status === 413) {
      this.openSnackBar('Your image was too large to upload', 'Close');
      this.data_loading = false;
      return;
    }

    this.openSnackBar('Uh Oh, something happened that made your upload fail', 'Close');
    this.data_loading = false;
  }

  private addAnalysisResult(response: any, type: string, message: string): void {
    const result = {
      thumbnail: response.thumbnail.replace('uploads', 'api'),
      openai_response: type === 'error' ? 'there was an error with the image analysis' : response.openai_response.choices[0].message.content,
      type
    };
    this.imageAnalysis = [result, ...this.imageAnalysis];
    this.openSnackBar(message, 'Close');
  }

  private openSnackBar(message: string, action: string): void {
    this.snackBar.open(message, action);
  }
}
