import { DateFormatPipe } from './date-format-pipe';

describe('DateFormatPipe', () => {
  let pipe: DateFormatPipe;

  beforeEach(() => {
    pipe = new DateFormatPipe();
  });

  it('should format date as shortDate', () => {
    const date = new Date('2025-08-26');
    expect(pipe.transform(date, 'shortDate')).toMatch(/\d{2}\/\d{2}\/\d{4}/);
  });

  it('should format date as longDate', () => {
    const date = new Date('2025-08-26');
    expect(pipe.transform(date, 'longDate')).toContain('2025');
  });

  it('should handle string date', () => {
    expect(pipe.transform('2025-08-26', 'shortDate')).toMatch(/\d{2}\/\d{2}\/\d{4}/);
  });

  it('should return empty string for null', () => {
    expect(pipe.transform(null)).toBe('');
  });
});