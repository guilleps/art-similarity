import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const influenceDict = [
  {
    percentage: 65.1,
    color: '#ff6b00',
    url: 'https://www.slobidka.com/images/rafael/Rafael_Sanzio-4.jpg'
  },
  {
    percentage: 32.5,
    color: '#a855f7',
    url: 'https://img.wikioo.org/ADC/Art-ImgScreen-4.nsf/O/A-8YDEXW/$FILE/Raphael-raffaello-sanzio-da-urbino-madonna-with-child-and-saints.Jpg'
  },
  {
    percentage: 18,
    color: '#f59e0b',
    url: 'https://www.slobidka.com/images/rafael/Rafael_Sanzio-21.jpg'
  }
]

export const stylePorcentage = [
  { percentage: 40, color: '#06b6d4' },
  { percentage: 30, color: '#a855f7' },
  { percentage: 15, color: '#ec4899' },
  { percentage: 15, color: '#22d3ee' }
]
